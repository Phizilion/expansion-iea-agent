from __future__ import annotations
from typing import List

from ._tool import tool

from config import SETTINGS

try:  # pragma: no cover - tested via absence
    from langchain_tavily import TavilySearchResults  # type: ignore
except Exception:  # pragma: no cover - the library is optional
    TavilySearchResults = None  # type: ignore

"""Tavily search tool with graceful fallback."""

if TavilySearchResults is not None:
    tavily_client = TavilySearchResults(
        tavily_api_key=SETTINGS.tavily_api_key, max_results=5
    )
else:  # pragma: no cover - exercised when dependency missing
    tavily_client = None


@tool("tavily_search", return_direct=False)
def tavily_search(query: str) -> List[dict]:
    """Search the web using Tavily.

    Returns a list of dictionaries containing ``title``, ``url`` and ``content``.
    When the Tavily client or API key is not configured, a single informative
    result is returned instead of raising an ImportError.
    """

    if tavily_client is None:
        return [
            {
                "title": "Tavily unavailable",
                "url": "",
                "content": "langchain_tavily not installed",
            }
        ]

    if not SETTINGS.tavily_api_key:
        return [
            {
                "title": "Tavily disabled",
                "url": "",
                "content": "No API key configured",
            }
        ]

    try:
        return tavily_client.invoke({"query": query})
    except Exception as e:  # pragma: no cover - network errors
        return [
            {
                "title": "Search error",
                "url": "",
                "content": f"{type(e).__name__}: {e}",
            }
        ]
