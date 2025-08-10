"""
Tool registry. Tools are individually importable and also exposed as a list
for quick binding to LLMs that support tool-calling via LangChain.
"""
from .web_search import tavily_search
from .browser import visit_url
from .fs_git import read_file, write_patch, run_tests, merge_and_reload
from .shell import safe_shell
from .http_client import http_get, http_post
from .parser import extract_text

TOOLS = [
    tavily_search,
    visit_url,
    read_file,
    write_patch,
    run_tests,
    merge_and_reload,
    safe_shell,
    http_get,
    http_post,
    extract_text,
]

__all__ = [t.name for t in TOOLS]  # type: ignore[attr-defined]
