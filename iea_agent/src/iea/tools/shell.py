from __future__ import annotations
from ._tool import tool
import shlex
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SAFE_BINARIES = {"ls","cat","wc","echo","grep","sed","awk","python","pytest","head","tail"}

@tool("safe_shell", return_direct=False)
def safe_shell(cmd: str) -> str:
    """
    Run a limited shell command from SAFE_BINARIES only.
    Example allowed: 'ls -la src/iea'
    """
    try:
        parts = shlex.split(cmd)
        if not parts:
            return "SHELL_ERROR: empty command"
        base = parts[0]
        if base not in SAFE_BINARIES:
            return f"SHELL_DENIED: '{base}' not in SAFE_BINARIES"
        p = subprocess.Popen(parts, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        out, _ = p.communicate(timeout=60)
        return f"RC={p.returncode}\n{out}"
    except Exception as e:
        return f"SHELL_EXCEPTION: {type(e).__name__}: {e}"
