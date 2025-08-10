from __future__ import annotations
from typing import Dict, Any, List
from llm import make_llm
from memory import search_knowledge, upsert_knowledge
from tools import TOOLS
from prompts import SYSTEM_INFO

from langchain_core.prompts import ChatPromptTemplate
INFO_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_INFO),
    ("human", "{payload}")
])

def run_info_exploration(question: str) -> Dict[str, Any]:
    """
    Single-shot information exploration run:
    - Fetch internal context
    - Bind tools and let the LLM decide if/what tools to use
    - Save synthesized result back to memory
    """
    from langchain_core.documents import Document
    llm = make_llm(purpose="research").bind_tools(TOOLS)
    internal_docs: List[Document] = search_knowledge(question, k=5)
    internal_snips = "\n\n".join([d.page_content[:1200] for d in internal_docs])
    content = f"INTERNAL_CONTEXT:\n{internal_snips}\n\nQUESTION:\n{question}"
    res = (INFO_PROMPT | llm).invoke({"payload": content})
    # Save synthesis; we only store up to 4KB per chunk to avoid huge vectors
    upsert_knowledge(str(res.content)[:4000], {"source": "info_exploration", "query": question})
    try:
        return res.dict()
    except Exception:
        return {"raw": res.content}
