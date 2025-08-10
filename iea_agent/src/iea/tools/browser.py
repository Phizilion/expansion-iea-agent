from __future__ import annotations
from langchain_core.tools import tool

"""
Simple Playwright-based page fetcher. This is *not* a crawler: it visits a single URL,
waits for DOMContentLoaded, extracts title and a small body snippet.
"""

@tool("visit_url", return_direct=False)
def visit_url(url: str) -> str:
    """
    Open a URL and return page title + snippet using headless Playwright.
    Errors are swallowed into returned string for agent awareness.
    """
    try:
        from playwright.sync_api import sync_playwright
        text_out = ""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            title = page.title()
            body = page.inner_text("body")[:1200]
            text_out = f"TITLE: {title}\nBODY_SNIPPET:\n{body}"
            browser.close()
        return text_out
    except Exception as e:
        return f"PLAYWRIGHT_ERROR: {type(e).__name__}: {e}"
