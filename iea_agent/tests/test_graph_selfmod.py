from iea.graphs.self_mod import build_self_mod_graph

def test_self_mod_compiles():
    g = build_self_mod_graph()
    init = {"goal":"Minor refactor", "file_list":["src/iea/memory/knowledge_base.py"], "last_result":"", "status":"start", "attempts":0}
    out = g.invoke(init)
    # We can't guarantee patching in CI, but graph should reach a terminal or loop state.
    assert out["status"] in {"patched","tested","merged","failed"}
