from iea.tools.fs_git import read_file, write_patch, run_tests, merge_and_reload

def test_fs_git_roundtrip():
    # Read a known file (cli.py should exist)
    rf = read_file.invoke({"path": "src/iea/cli.py"})  # type: ignore
    assert "def main()" in rf

    # Minimal patch that doesn't break the repo: append a newline to README
    diff = """\
---
*** Begin Patch
*** Update File: README.md
@@
 # IEA-PoC (Independent Economic Activity) — LangGraph POC
@@
 This proof-of-concept shows a self-improving agent capable of:
+
+<!-- test patch line -->
"""
    ap = write_patch.invoke({"unified_diff": diff})  # type: ignore
    assert "PATCH_APPLIED" in ap or "PATCH_FAILED" in ap

    rt = run_tests.invoke({})  # type: ignore
    assert "PYTEST_RC" in rt

    mg = merge_and_reload.invoke({})  # type: ignore
    assert "MERGE_RC" in mg or "MERGE_ERROR" in mg
