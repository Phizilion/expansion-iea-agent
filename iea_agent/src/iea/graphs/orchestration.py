from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import json
import logging
from .targeting import build_targeting_graph, TargetState
from .self_mod import build_self_mod_graph, SelfModState
from .info import run_info_exploration

log = logging.getLogger("iea.orchestration")

@dataclass
class Orchestrator:
    """
    Orchestrator glues together the three abilities in a minimal way:
    - run_targeting(goal)
    - run_info(query)
    - run_self_mod(goal, files)
    """
    def run_targeting(self, goal: str) -> Dict[str, Any]:
        g = build_targeting_graph()
        state: TargetState = {"target": goal, "tasks": [], "current": None, "mode": "decide_or_plan", "log": []}
        final = g.invoke(state)
        return {
            "mode": final["mode"],
            "log": final["log"],
            "tasks_remaining": final.get("tasks", []),
        }

    def run_info(self, query: str) -> Dict[str, Any]:
        return run_info_exploration(query)

    def run_self_mod(self, goal: str, files: str) -> Dict[str, Any]:
        g = build_self_mod_graph()
        init: SelfModState = {"goal": goal, "file_list": files.split(","), "last_result": "", "status": "start", "attempts": 0}
        out = g.invoke(init)
        return {"status": out["status"], "last_result": out["last_result"][-2000:]}
