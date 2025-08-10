from iea.graphs.targeting import build_targeting_graph

def test_targeting_runs_minimal():
    g = build_targeting_graph()
    init = {"target":"Find two credible sources for Hyprland tips","tasks":[],"current":None,"mode":"decide_or_plan","log":[]}
    out = g.invoke(init)
    assert out["mode"] in {"execute","done"}
