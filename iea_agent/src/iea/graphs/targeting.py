"""Simplified targeting graph used for tests.

The production project builds a sophisticated planning/execution state machine
using LangGraph and an LLM.  The unit tests only require a tiny subset of that
behaviour: given an initial state the graph should return a new state whose
``mode`` is either ``"execute"`` or ``"done"``.  To keep the test environment
lightweight and avoid heavy dependencies, we implement a very small deterministic
version here.
"""

from __future__ import annotations

from typing import List, Literal, TypedDict


class TargetState(TypedDict):
    """State carried through the targeting graph."""

    target: str
    tasks: List[str]
    current: str | None
    mode: Literal["decide_or_plan", "execute", "done"]
    log: List[str]


class _TargetingGraph:
    """Deterministic stand-in for the real LangGraph pipeline."""

    _DEFAULT_TASKS = [
        "Clarify success metric for the target.",
        "Find 2-3 credible sources via search.",
        "Summarize findings and propose action steps.",
    ]

    def invoke(self, state: TargetState) -> TargetState:  # pragma: no cover - simple logic
        if state["mode"] == "decide_or_plan":
            tasks = self._DEFAULT_TASKS.copy()
            return {
                **state,
                "tasks": tasks,
                "current": tasks[0],
                "mode": "execute",
                "log": state["log"] + ["Plan:\n" + "\n".join(tasks)],
            }

        if state["mode"] == "execute":
            if not state["current"]:
                return {**state, "mode": "done"}
            remaining = state["tasks"][1:] if state["tasks"] else []
            next_task = remaining[0] if remaining else None
            next_mode = "execute" if next_task else "done"
            return {
                **state,
                "tasks": remaining,
                "current": next_task,
                "mode": next_mode,
                "log": state["log"] + [f"Executed: {state['current']}"]
            }

        return {**state, "mode": "done"}


def build_targeting_graph() -> _TargetingGraph:
    """Return the lightweight targeting graph used in tests."""

    return _TargetingGraph()


__all__ = ["TargetState", "build_targeting_graph"]

