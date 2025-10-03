# Author: everettjf
"""Tests for the LangGraph-powered planner core."""

from __future__ import annotations

import os

os.environ.setdefault("LANGCHAIN_TRACING_V2", "false")
os.environ.setdefault("LANGSMITH_TRACING", "false")

import langsmith.utils as langsmith_utils

langsmith_utils.tracing_enabled = lambda: False
langsmith_utils.tracing_v2_enabled = lambda: False

from ideaforge.planner import IdeaPlanner, PlanNode, PlanResult


class StaticPlannerModel:
    def __init__(self, plan):
        self.plan = plan

    def invoke(self, *_args, **_kwargs):
        return {"plan": self.plan}


class SequenceReactModel:
    def __init__(self, payloads):
        self.payloads = payloads
        self.calls = 0

    def invoke(self, *_args, **_kwargs):
        payload = self.payloads[self.calls]
        self.calls += 1
        return payload


def test_plan_generates_tree_and_launch_step():
    plan_skeleton = [
        {
            "title": "Validate the opportunity",
            "summary": "Research users and define value props.",
            "deliverable": "Problem/solution brief",
            "tasks": [],
        },
        {
            "title": "Build MVP",
            "summary": "Implement the core user experience.",
            "deliverable": "Functional MVP",
            "tasks": [],
        },
    ]

    react_payloads = [
        {
            "analysis": [
                "Thought: interview prospective users",
                "Action: draft research script",
                "Observation: script ready",
                "Thought: summarize findings",
                "Final: problem framing locked",
            ],
            "tasks": [
                {
                    "title": "User interviews",
                    "summary": "Conduct 5 interviews to validate the pain points.",
                    "deliverable": "Insights report",
                    "tasks": [],
                },
                {
                    "title": "Value proposition memo",
                    "summary": "Summarize the opportunity and success metrics.",
                    "deliverable": "Internal alignment memo",
                    "tasks": [],
                },
            ],
        },
        {
            "analysis": [
                "Thought: prioritize backlog",
                "Action: implement core flows",
                "Observation: tests green",
                "Final: MVP ready",
            ],
            "tasks": [
                {
                    "title": "Design to dev handoff",
                    "summary": "Finalize UI kit and flows for developers.",
                    "deliverable": "Build-ready Figma",
                    "tasks": [],
                },
                {
                    "title": "Implement backend",
                    "summary": "Set up API and database with auth.",
                    "deliverable": "Stable backend",
                    "tasks": [
                        {
                            "title": "Provision infrastructure",
                            "summary": "Bootstrap staging environment with IaC.",
                            "deliverable": "Ready environments",
                            "tasks": [],
                        }
                    ],
                },
            ],
        },
    ]

    planner = IdeaPlanner(StaticPlannerModel(plan_skeleton), SequenceReactModel(react_payloads))
    result: PlanResult = planner.plan("Social habit tracker app")

    assert isinstance(result, PlanResult)
    assert len(result.tree) == 3  # launch step appended automatically

    launch_node = result.tree[-1]
    assert launch_node.title == "Launch & Post-Launch"
    assert all(isinstance(node, PlanNode) for node in result.tree)

    # Ensure ReAct traces were captured for the first two tasks only
    assert len(result.analyses) == 2
    assert result.analyses[0].startswith("Validate the opportunity")

    # Ensure nested subtasks remained intact
    backend_node = result.tree[1].tasks[1]
    assert backend_node.tasks[0].title == "Provision infrastructure"



def test_plan_reports_progress_updates():
    plan_skeleton = [
        {
            "title": "Build MVP",
            "summary": "Implement the first release scope.",
            "deliverable": "MVP",
            "tasks": [],
        }
    ]
    react_payloads = [
        {
            "analysis": ["Thought: plan work", "Final: ready"],
            "tasks": [
                {
                    "title": "Implement feature set",
                    "summary": "Build core flows and tests.",
                    "deliverable": "Implemented MVP",
                    "tasks": [],
                }
            ],
        }
    ]
    planner = IdeaPlanner(StaticPlannerModel(plan_skeleton), SequenceReactModel(react_payloads))
    messages: list[str] = []
    planner.plan("Progress demo", progress=messages.append)

    assert messages[0] == "Generating roadmap outline"
    assert any(msg.startswith("Refining objective") for msg in messages)
    assert "Ensuring launch coverage" in messages
    assert messages[-1] == "Launch plan ready"
