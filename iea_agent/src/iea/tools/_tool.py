"""Lightweight stand-in for ``langchain_core.tools.tool``.

The production project relies on LangChain's ``@tool`` decorator to provide
metadata for tool-calling LLMs.  The tests in this kata don't require the full
LangChain dependency, so we provide a very small shim that simply returns the
decorated function unchanged when LangChain isn't installed.
"""

from __future__ import annotations

try:  # pragma: no cover - real dependency if available
    from langchain_core.tools import tool as lc_tool  # type: ignore
except Exception:  # pragma: no cover - fallback path used in tests
    lc_tool = None  # type: ignore


def tool(name: str | None = None, return_direct: bool | None = None):
    """Fallback ``tool`` decorator compatible with LangChain's signature."""

    if lc_tool is not None:  # use real decorator when available
        return lc_tool(name, return_direct=return_direct)

    def decorator(func):  # type: ignore[override]
        func.name = name or func.__name__  # mimic LangChain attribute

        def invoke(args):  # simple interface matching LangChain tools
            if isinstance(args, dict):
                return func(**args)
            return func(args)

        func.invoke = invoke  # type: ignore[attr-defined]
        return func

    return decorator


__all__ = ["tool"]

