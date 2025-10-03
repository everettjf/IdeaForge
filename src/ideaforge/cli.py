# Author: everettjf
"""Command line interface for the IdeaForge planner."""

from __future__ import annotations

import os
import sys
from typing import Optional

import typer
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.panel import Panel

from .planner import IdeaPlanner, PlanNode, PlanResult

cli_app = typer.Typer(help="Generate launch-ready TODO trees for product ideas.")
console = Console()


def _build_model(model: str, temperature: float, api_key: Optional[str]) -> ChatOpenAI:
    kwargs = {"model": model, "temperature": temperature}
    if api_key:
        kwargs["api_key"] = api_key
    return ChatOpenAI(**kwargs)


def _build_planner(
    plan_model: str,
    react_model: Optional[str],
    temperature: float,
    react_temperature: Optional[float],
    api_key: str,
) -> IdeaPlanner:
    planner_llm = _build_model(plan_model, temperature, api_key)
    executor_llm = _build_model(react_model or plan_model, react_temperature or min(0.6, temperature + 0.2), api_key)
    return IdeaPlanner(planner_llm, executor_llm)


def _render_tree(tree: list[PlanNode]) -> str:
    lines: list[str] = []
    for index, node in enumerate(tree):
        lines.extend(node.render(is_last=index == len(tree) - 1))
    return "\n".join(lines)


@cli_app.command(name="plan")
def plan_command(
    idea: str = typer.Argument(..., help="One-line description of the product idea."),
    plan_model: str = typer.Option("gpt-4o-mini", help="Model used for the planning pass."),
    react_model: Optional[str] = typer.Option(None, help="Optional override for the ReAct execution model."),
    temperature: float = typer.Option(0.2, help="Base temperature for plan generation."),
    react_temperature: Optional[float] = typer.Option(None, help="Temperature for the execute/ReAct stage."),
    show_analysis: bool = typer.Option(True, help="Display ReAct reasoning traces."),
) -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[bold yellow]OPENAI_API_KEY is not set. Enter it now to continue.[/bold yellow]")
        api_key = typer.prompt("OpenAI API key", hide_input=True, show_default=False).strip()
        if not api_key:
            console.print("[bold red]An OpenAI API key is required to run IdeaForge.")
            raise typer.Exit(code=1)
        os.environ["OPENAI_API_KEY"] = api_key

    planner = _build_planner(plan_model, react_model, temperature, react_temperature, api_key)
    console.print(Panel.fit(f"Idea: {idea}", title="IdeaForge", border_style="cyan"))
    progress_log: list[str] = []

    def handle_progress(message: str) -> None:
        if not message:
            return
        status.update(f"[bold cyan]Working[/bold cyan] {message}")
        if not progress_log or progress_log[-1] != message:
            progress_log.append(message)
            status.console.print(f"[bold cyan]Working[/bold cyan] {message}")

    with console.status("[bold cyan]Working[/bold cyan] Generating roadmap...", spinner="dots") as status:
        result: PlanResult = planner.plan(idea, progress=handle_progress)
    console.print(Panel(_render_tree(result.tree), title="Launch TODO Tree", border_style="green"))
    if show_analysis and result.analyses:
        analysis_text = "\n".join(f"- {entry}" for entry in result.analyses)
        console.print(Panel(analysis_text, title="ReAct Analysis", border_style="magenta"))


def main() -> None:  # pragma: no cover - thin wrapper for entry point
    if len(sys.argv) > 1 and sys.argv[1].lower() == "plan":
        sys.argv.pop(1)
    cli_app()


if __name__ == "__main__":  # pragma: no cover
    main()
