from __future__ import annotations
import subprocess
from pathlib import Path
from langchain_core.tools import tool

"""
File-system + Git tools used by the self-modification pipeline.
Operations are scoped to the repository root to avoid path traversal.

NOTE: For a fresh repo inside container, we ensure 'git init' and a main branch exist.
"""

REPO_ROOT = Path(__file__).resolve().parents[2]

def _run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.Popen(cmd, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out, _ = p.communicate()
    return p.returncode, out

def _ensure_git():
    _run(["git", "init"])
    _run(["git", "config", "user.email", "iea@example.com"])
    _run(["git", "config", "user.name", "IEA Agent"])
    # Create main branch if not present
    _run(["git", "checkout", "-B", "main"])
    _run(["git", "add", "-A"])
    _run(["git", "commit", "-m", "iea: snapshot", "--allow-empty"])

@tool("read_file", return_direct=False)
def read_file(path: str) -> str:
    """
    Read a UTF-8 file from repo root safely.
    """
    abs_path = (REPO_ROOT / path).resolve()
    if not abs_path.is_file() or REPO_ROOT not in abs_path.parents:
        return "ERROR: invalid path"
    try:
        return abs_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"READ_ERROR: {type(e).__name__}: {e}"

@tool("write_patch", return_direct=False)
def write_patch(unified_diff: str) -> str:
    """
    Apply a unified diff to the repo in a temp branch 'iea/temp-change'.
    """
    try:
        _ensure_git()
        _run(["git", "checkout", "-B", "iea/temp-change"])
        patch_proc = subprocess.run(
            ["git", "apply", "--whitespace=fix", "-p0"],
            input=unified_diff, text=True, cwd=REPO_ROOT,
            capture_output=True
        )
        if patch_proc.returncode != 0:
            return f"PATCH_FAILED:\nSTDERR:\n{patch_proc.stderr}\nSTDOUT:\n{patch_proc.stdout}"
        _run(["git", "add", "-A"])
        code, out = _run(["git", "commit", "-m", "iea: apply patch"])
        return f"PATCH_APPLIED rc={code}\n{out}"
    except Exception as e:
        return f"PATCH_TOOL_ERROR: {type(e).__name__}: {e}"

@tool("run_tests", return_direct=False)
def run_tests() -> str:
    """
    Run pytest and return summary lines including RC.
    """
    try:
        code, out = _run(["pytest", "-q"])
        return f"PYTEST_RC={code}\n{out}"
    except Exception as e:
        return f"RUN_TESTS_ERROR: {type(e).__name__}: {e}"

@tool("merge_and_reload", return_direct=False)
def merge_and_reload() -> str:
    """
    Merge temp branch back to main; in a real system, we'd also hot-reload modules.
    Here we limit to merge for safety.
    """
    try:
        _ensure_git()
        _run(["git", "checkout", "-B", "main"])
        code, out = _run(["git", "merge", "--no-ff", "iea/temp-change", "-m", "iea: merge temp-change"])
        return f"MERGE_RC={code}\n{out}"
    except Exception as e:
        return f"MERGE_ERROR: {type(e).__name__}: {e}"
