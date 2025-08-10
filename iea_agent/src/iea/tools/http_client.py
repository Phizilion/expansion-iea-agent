from __future__ import annotations
from ._tool import tool

try:  # pragma: no cover - optional dependency
    import httpx  # type: ignore
except Exception:  # pragma: no cover - httpx may be missing
    httpx = None  # type: ignore

@tool("http_get", return_direct=False)
def http_get(url: str) -> str:
    """
    Make a simple GET request with httpx and return status + short body.
    """
    if httpx is None:
        return "HTTP_GET_ERROR: httpx not installed"
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
    if httpx is None:
        return "HTTP_POST_ERROR: httpx not installed"
    try:
        r = httpx.post(url, content=json_payload, headers={"Content-Type":"application/json"}, timeout=20)
        return f"STATUS={r.status_code}\n{r.text[:1200]}"
    except Exception as e:
        return f"HTTP_POST_ERROR: {type(e).__name__}: {e}"
