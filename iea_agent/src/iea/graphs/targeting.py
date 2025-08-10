from __future__ import annotations
from typing import TypedDict, List, Literal
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from ..llm import make_llm
from ..tools import TOOLS
from ..memory import upsert_knowledge
from ..prompts import SYSTEM_TARGETING, SYSTEM_EXECUTOR

class TargetState(TypedDict):
    """
    State carried through the Targeting graph.
    """
    target: str
    tasks: List[str]
    current: str | None
    mode: Literal["decide_or_plan","execute","done"]
    log: List[str]

DECIDE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_TARGETING),
    ("human", "{target}")
])

EXEC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_EXECUTOR),
    ("human", "{task}")
])

def build_targeting_graph():
    """
    Build a LangGraph with two main nodes:
    - decide_or_plan
    - execute
    The graph starts with decide_or_plan, possibly transitions to execute,
    and loops until all tasks are done.
    """
    graph = StateGraph(TargetState)
    llm_decide = make_llm(purpose="plan")
    llm_exec = make_llm(purpose="execute").bind_tools(TOOLS)

    def decide_or_plan(state: TargetState) -> TargetState:
        out = (DECIDE_PROMPT | llm_decide).invoke({"target": state["target"]}).content
        # Heuristic: If the model says "EXECUTE:" choose direct execution, else parse tasks
        if "EXECUTE:" in out.upper():
            return {**state, "current": state["target"], "mode": "execute", "log": state["log"] + [f"Decision: execute\n{out}"]}

        # Parse lines into tasks
        lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
        tasks = []
        for ln in lines:
            # strip bullets
            if ln.startswith(("-", "*", "•")):
                ln = ln.lstrip("-*• ").strip()
            tasks.append(ln)
        # constrain to 3-7 tasks, fallback if model misbehaves
        if len(tasks) < 3:
            # produce a quick minimal plan
            tasks = [
                "Clarify success metric for the target.",
                "Find 2-3 credible sources via search.",
                "Summarize findings and propose action steps."
            ]
        tasks = tasks[:7]
        return {**state, "tasks": tasks, "current": tasks[0], "mode": "execute", "log": state["log"] + [f"Plan:\n" + "\n".join(tasks)]}

    def execute(state: TargetState) -> TargetState:
        if not state["current"]:
            return {**state, "mode": "done"}
        res = (EXEC_PROMPT | llm_exec).invoke({"task": state["current"]})
        content = res.content or ""
        # persist partial results as knowledge to improve subsequent steps
        upsert_knowledge(content[:4000], {"source": "execution", "task": state["current"]})
        remaining = state["tasks"][1:] if state["tasks"] else []
        next_task = remaining[0] if remaining else None
        next_mode = "execute" if next_task else "done"
        return {
            **state,
            "tasks": remaining,
            "current": next_task,
            "mode": next_mode,
            "log": state["log"] + [f"Executed: {state['current']}\n{content[:1200]}"]
        }

    graph.add_node("decide_or_plan", decide_or_plan)
    graph.add_node("execute", execute)

    graph.set_entry_point("decide_or_plan")
    graph.add_conditional_edges(
        "decide_or_plan",
        lambda s: "execute" if s["mode"] == "execute" else ("done" if s["mode"] == "done" else "execute"),
        {"execute": "execute", "done": END}
    )
    graph.add_conditional_edges(
        "execute",
        lambda s: "execute" if s["mode"] == "execute" else "done",
        {"execute": "execute", "done": END}
    )

    return graph.compile()
