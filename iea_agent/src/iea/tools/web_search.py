from __future__ import annotations
from typing import List
from langchain_tavily import TavilySearchResults
from langchain_core.tools import tool
from ..config import SETTINGS

"""
Tavily search tool.
We use the lightweight `TavilySearchResults` wrapper from LangChain that returns
structured results for a given query.
"""

tavily = TavilySearchResults(tavily_api_key=SETTINGS.tavily_api_key, max_results=5)

@tool("tavily_search", return_direct=False)
def tavily_search(query: str) -> List[dict]:
    """
    Search the web with Tavily and return top results with URLs & snippets.
    Input: query (str)
    Output: List[dict] with keys: 'title', 'url', 'content' (snippet)
    """
    if not SETTINGS.tavily_api_key:
        return [{"title": "Tavily disabled", "url": "", "content": "No API key configured"}]
    try:
        return tavily.invoke({"query": query})
    except Exception as e:
        return [{"title": "Search error", "url": "", "content": f"{type(e).__name__}: {e}"}]
