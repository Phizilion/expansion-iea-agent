from __future__ import annotations
from langchain_core.tools import tool
import httpx

@tool("http_get", return_direct=False)
def http_get(url: str) -> str:
    """
    Make a simple GET request with httpx and return status + short body.
    """
    try:
        r = httpx.get(url, timeout=15)
        return f"STATUS={r.status_code}\n{r.text[:1200]}"
    except Exception as e:
        return f"HTTP_GET_ERROR: {type(e).__name__}: {e}"

@tool("http_post", return_direct=False)
def http_post(url: str, json_payload: str) -> str:
    """
    POST JSON string payload and return status + short response.
    """
    try:
        r = httpx.post(url, content=json_payload, headers={"Content-Type":"application/json"}, timeout=20)
        return f"STATUS={r.status_code}\n{r.text[:1200]}"
    except Exception as e:
        return f"HTTP_POST_ERROR: {type(e).__name__}: {e}"
