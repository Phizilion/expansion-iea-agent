from __future__ import annotations
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from ..llm import make_llm
from ..tools import read_file, write_patch, run_tests, merge_and_reload
from ..prompts import SYSTEM_SELF_MOD

class SelfModState(TypedDict):
    goal: str
    file_list: list[str]
    last_result: str
    status: Literal["start","patched","tested","merged","failed"]
    attempts: int

def build_self_mod_graph():
    """
    Self-modification graph:
    propose_patch -> test_changes -> evaluate -> (loop or merged/failed)
    """
    graph = StateGraph(SelfModState)
    llm = make_llm(purpose="code").bind_tools([read_file, write_patch, run_tests, merge_and_reload])

    def propose_patch(state: SelfModState) -> SelfModState:
        prompt = [
            SystemMessage(content=SYSTEM_SELF_MOD),
            HumanMessage(content=f"SELF-MOD GOAL: {state['goal']}\nFILES: {state['file_list']}\nLAST_RESULT:\n{state['last_result'][-1800:]}"),
        ]
        msg = llm.invoke(prompt)
        return {**state, "last_result": msg.content, "status": "patched"}

    def test_changes(state: SelfModState) -> SelfModState:
        # We expect the last_result to carry a diff. Ask model to call tools to apply & test.
        msg = llm.invoke([HumanMessage(content="Apply the diff using write_patch (tool), then run_tests (tool). Return outputs.")])
        return {**state, "last_result": getattr(msg, "content", ""), "status": "tested"}

    def evaluate(state: SelfModState) -> SelfModState:
        out = state["last_result"]
        if "PYTEST_RC=0" in out:
            m = llm.invoke([HumanMessage(content="All tests passed. Call merge_and_reload tool.")])
            return {**state, "last_result": getattr(m, "content", ""), "status": "merged"}
        if state["attempts"] >= 3:
            return {**state, "status": "failed"}
        ref = llm.invoke([HumanMessage(content=f"Tests failing. Improve the diff and try again.\nFAIL LOG (tail):\n{out[-1600:]}" )])
        return {**state, "last_result": getattr(ref, "content", ""), "attempts": state["attempts"]+1, "status": "patched"}

    graph.add_node("propose_patch", propose_patch)
    graph.add_node("test_changes", test_changes)
    graph.add_node("evaluate", evaluate)

    graph.set_entry_point("propose_patch")
    graph.add_edge("propose_patch", "test_changes")
    graph.add_edge("test_changes", "evaluate")
    graph.add_conditional_edges(
        "evaluate",
        lambda s: "end" if s["status"] in ["merged","failed"] else "propose_patch",
        {"end": END, "propose_patch": "propose_patch"}
    )
    return graph.compile()
