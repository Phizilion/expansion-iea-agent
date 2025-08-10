"""Minimal self-modification graph for the test environment.

The full project uses LangGraph and an LLM to iteratively propose code patches,
run tests and merge changes.  For unit testing we only need a skeleton that
exposes the same interface without external dependencies.  This module provides
that lightweight stand-in.
"""

from __future__ import annotations

from typing import Literal, TypedDict


class SelfModState(TypedDict):
    goal: str
    file_list: list[str]
    last_result: str
    status: Literal["start", "patched", "tested", "merged", "failed"]
    attempts: int


class _SelfModGraph:
    """Very small state machine used in tests."""

    def invoke(self, state: SelfModState) -> SelfModState:  # pragma: no cover
        if state["status"] == "start":
            return {**state, "status": "patched", "last_result": "patch diff"}
        if state["status"] == "patched":
            return {**state, "status": "tested", "last_result": "PYTEST_RC=0"}
        if state["status"] == "tested":
            return {**state, "status": "merged"}
        return {**state, "status": "failed"}


def build_self_mod_graph() -> _SelfModGraph:
    """Return the lightweight self-modification graph."""

    return _SelfModGraph()


__all__ = ["SelfModState", "build_self_mod_graph"]

