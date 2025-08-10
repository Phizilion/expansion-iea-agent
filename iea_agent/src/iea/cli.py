from __future__ import annotations
from .env import *  # load .env early
from .logging import setup_logging
from .graphs import Orchestrator
import typer
from rich import print

app = typer.Typer(add_completion=False)

@app.callback()
def main():
    setup_logging()

@app.command()
def target(goal: str):
    """
    Run the Targeting loop on a goal.
    """
    orch = Orchestrator()
    res = orch.run_targeting(goal)
    print("[bold green]Targeting log:[/bold green]")
    for entry in res["log"]:
        head = entry.splitlines()[0]
        print(f"- {head}")
    print("\n[bold]Final mode:[/bold]", res["mode"])
    if res["tasks_remaining"]:
        print("[yellow]Remaining tasks:[/yellow]", res["tasks_remaining"])

@app.command()
def brief(topic: str):
    """
    Run the Information Exploration pipeline for a topic (and save to memory).
    """
    orch = Orchestrator()
    out = orch.run_info(topic)
    print(out)

@app.command()
def selfmod(goal: str, files: str = "src/iea/*.py"):
    """
    Run the self-modification cycle for a small refactor or fix across target files.
    """
    orch = Orchestrator()
    res = orch.run_self_mod(goal, files)
    print(res["status"])
    print(res["last_result"])

if __name__ == "__main__":
    app()
