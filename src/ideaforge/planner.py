# Author: everettjf
"""LangGraph-powered planner for turning ideas into launch-ready TODO trees."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.base import Runnable
from langgraph.graph import END, START, StateGraph


class PlannerState(TypedDict, total=False):
    """Mutable state that flows through the planning LangGraph."""

    idea: str
    plan: List[Dict[str, Any]]
    current_index: int
    analyses: List[str]


@dataclass
class PlanNode:
    """Node in the hierarchical TODO tree."""

    title: str
    summary: str = ""
    deliverable: str = ""
    tasks: List["PlanNode"] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlanNode":
        tasks = [cls.from_dict(child) for child in data.get("tasks", [])]
        return cls(
            title=data.get("title", "Untitled"),
            summary=data.get("summary", ""),
            deliverable=data.get("deliverable", ""),
            tasks=tasks,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "summary": self.summary,
            "deliverable": self.deliverable,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    def iter_nodes(self) -> Iterable["PlanNode"]:
        yield self
        for child in self.tasks:
            yield from child.iter_nodes()

    def render(self, prefix: str = "", is_last: bool = True) -> List[str]:
        connector = "└── " if is_last else "├── "
        headline = f"{self.title}"
        if self.deliverable:
            headline += f" → {self.deliverable}"
        lines = [f"{prefix}{connector}{headline}"]
        detail_prefix = "    " if is_last else "│   "
        if self.summary:
            lines.append(f"{prefix}{detail_prefix}summary: {self.summary}")
        for index, child in enumerate(self.tasks):
            lines.extend(child.render(prefix + detail_prefix, index == len(self.tasks) - 1))
        return lines


PlanTree = List[PlanNode]


@dataclass
class PlanResult:
    tree: PlanTree
    analyses: List[str]


class IdeaPlanner:
    """High-level wrapper around a LangGraph plan-and-execute pipeline."""

    def __init__(
        self,
        planner_model: Runnable,
        react_model: Runnable,
    ) -> None:
        self._planner_model = planner_model
        self._react_model = react_model
        self._graph = self._build_graph()
        self._progress_callback: Callable[[str], None] | None = None

    def plan(self, idea: str, progress: Callable[[str], None] | None = None) -> PlanResult:
        previous_callback = self._progress_callback
        self._progress_callback = progress
        self._emit_progress("Generating roadmap outline")
        state: PlannerState = {"idea": idea}
        try:
            result = self._graph.invoke(state)
            self._emit_progress("Finalizing launch plan")
            plan_dicts = result["plan"]
            analyses = result.get("analyses", [])
            tree = [PlanNode.from_dict(item) for item in plan_dicts]
            self._emit_progress("Launch plan ready")
            return PlanResult(tree=tree, analyses=analyses)
        finally:
            self._progress_callback = previous_callback

    def _build_graph(self):
        graph: StateGraph[PlannerState] = StateGraph(PlannerState)

        graph.add_node("plan", self._plan_node)
        graph.add_node("react", self._react_node)
        graph.add_node("finalize", self._finalize_node)

        graph.add_edge(START, "plan")
        graph.add_conditional_edges("plan", self._plan_has_items, {True: "react", False: "finalize"})
        graph.add_conditional_edges("react", self._should_continue, {True: "react", False: "finalize"})
        graph.add_edge("finalize", END)

        return graph.compile()

    def _emit_progress(self, message: str) -> None:
        if self._progress_callback:
            self._progress_callback(message)

    def _plan_has_items(self, state: PlannerState) -> bool:
        return bool(state.get("plan"))

    def _should_continue(self, state: PlannerState) -> bool:
        current = state.get("current_index", 0)
        plan = state.get("plan", [])
        return current < len(plan)

    def _plan_node(self, state: PlannerState) -> PlannerState:
        idea = state["idea"]
        messages = [
            SystemMessage(
                content=(
                    "You are a senior product builder. Craft high-level launch roadmaps that end in a shipped app or web product.\n"
                    "Return strict JSON only."
                )
            ),
            HumanMessage(
                content=(
                    "Idea: "
                    + idea
                    + "\nProduce JSON with key plan -> list of 3-5 ordered objects."
                    " Each object must include title, summary, deliverable, tasks (empty list initially)."
                    " Focus on 2-3 levels total when tasks are later expanded."
                )
            ),
        ]
        response = self._planner_model.invoke(messages)
        plan_dict = self._coerce_to_json(response)
        plan_items = plan_dict.get("plan")
        if not isinstance(plan_items, list) or not plan_items:
            raise ValueError("Planner model did not return a non-empty plan list")
        self._emit_progress(f"Captured {len(plan_items)} top-level objectives")
        return {
            **state,
            "plan": plan_items,
            "current_index": 0,
            "analyses": [],
        }

    def _react_node(self, state: PlannerState) -> PlannerState:
        plan = state["plan"]
        index = state.get("current_index", 0)
        target = plan[index]
        total = len(plan)
        self._emit_progress(
            f"Refining objective {index + 1}/{total}: {target.get('title', 'Objective')}"
        )
        messages = [
            SystemMessage(
                content=(
                    "You are the execute agent in a plan-and-execute loop."
                    " Follow a ReAct style: alternate thought and action to stress-test and expand the plan."
                    " Always end with Final Answer JSON."
                )
            ),
            HumanMessage(
                content=(
                    "Idea: "
                    + state["idea"]
                    + "\nTop-level objective: "
                    + target.get("title", "")
                    + "\nSummary: "
                    + target.get("summary", "")
                    + "\nDeliverable: "
                    + target.get("deliverable", "")
                    + "\nExisting tasks: "
                    + json.dumps(target.get("tasks", []))
                    + "\nThink through preparation, implementation, validation, and launch readiness."
                    " Provide a JSON object with keys analysis (list of strings capturing the ReAct steps)"
                    " and tasks (list of child task objects with title, summary, deliverable, tasks)."
                    " Ensure child tasks cover everything necessary for this objective and include any final"
                    " steps required to reach production. Allow third-level subtasks when helpful."
                )
            ),
        ]
        response = self._react_model.invoke(messages)
        payload = self._coerce_to_json(response)
        analysis = payload.get("analysis", [])
        tasks = payload.get("tasks", [])
        if not isinstance(tasks, list) or not tasks:
            raise ValueError("ReAct model must return non-empty tasks list")
        plan[index]["tasks"] = tasks
        analyses = state.get("analyses", []) + [self._format_analysis(target.get("title", ""), analysis)]
        self._emit_progress(f"Completed objective {index + 1}/{total}")
        return {
            **state,
            "plan": plan,
            "current_index": index + 1,
            "analyses": analyses,
        }

    def _finalize_node(self, state: PlannerState) -> PlannerState:
        plan = state.get("plan", [])
        if not plan:
            raise ValueError("Finalization received empty plan")
        self._emit_progress("Ensuring launch coverage")
        self._ensure_release_step(plan)
        return state

    def _ensure_release_step(self, plan: List[Dict[str, Any]]) -> None:
        release_keywords = ("launch", "release", "deploy", "submission", "publish")
        for item in plan:
            if self._contains_release(item, release_keywords):
                return
        plan.append(
            {
                "title": "Launch & Post-Launch",
                "summary": "Prepare stores, deploy infrastructure, and set up analytics to monitor the release.",
                "deliverable": "Live product available to target users",
                "tasks": [
                    {
                        "title": "App store / web deployment",
                        "summary": "Publish to the chosen distribution channel with production configurations.",
                        "deliverable": "Public release",
                        "tasks": [],
                    },
                    {
                        "title": "Post-launch instrumentation",
                        "summary": "Set up monitoring, analytics, and incident response routines.",
                        "deliverable": "Operational readiness",
                        "tasks": [],
                    },
                ],
            }
        )

    def _contains_release(self, item: Dict[str, Any], keywords: Iterable[str]) -> bool:
        text = " ".join(
            str(part).lower()
            for part in [item.get("title"), item.get("summary"), item.get("deliverable")]
            if part
        )
        if any(keyword in text for keyword in keywords):
            return True
        for child in item.get("tasks", []) or []:
            if self._contains_release(child, keywords):
                return True
        return False

    def _format_analysis(self, title: str, analysis: Any) -> str:
        if isinstance(analysis, list):
            cleaned = " | ".join(str(step).strip() for step in analysis if step)
            return f"{title}: {cleaned}" if cleaned else title
        return f"{title}: {analysis}"

    def _coerce_to_json(self, response: Any) -> Dict[str, Any]:
        if isinstance(response, dict):
            return response
        if hasattr(response, "content"):
            payload = response.content  # type: ignore[attr-defined]
        else:
            payload = response
        text = self._stringify_content(payload)
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.startswith("```json"):
            text = text[len("```json") :]
        text = text.strip("`\n ")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            candidate = self._extract_first_json_block(text)
            if candidate is not None:
                return json.loads(candidate)
            raise ValueError(f"Model did not return valid JSON: {text}")

    def _extract_first_json_block(self, text: str) -> str | None:
        for opener, closer in ('{}', '[]'):
            stack = 0
            start = None
            for index, char in enumerate(text):
                if char == opener:
                    if stack == 0:
                        start = index
                    stack += 1
                elif char == closer and stack:
                    stack -= 1
                    if stack == 0 and start is not None:
                        candidate = text[start:index + 1]
                        try:
                            json.loads(candidate)
                        except json.JSONDecodeError:
                            continue
                        return candidate
        return None

    def _stringify_content(self, payload: Any) -> str:
        if isinstance(payload, str):
            return payload
        if isinstance(payload, list):
            parts: List[str] = []
            for chunk in payload:
                if isinstance(chunk, str):
                    parts.append(chunk)
                elif isinstance(chunk, dict) and "text" in chunk:
                    parts.append(str(chunk["text"]))
                else:
                    parts.append(str(chunk))
            return "".join(parts)
        return str(payload)


__all__ = ["IdeaPlanner", "PlanTree", "PlanNode", "PlanResult"]
