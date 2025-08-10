from __future__ import annotations
from typing import Optional, Iterable

try:  # pragma: no cover - dependency may be absent
    from langchain_core.documents import Document  # type: ignore
except Exception:  # pragma: no cover
    from .vectorstore import Document  # type: ignore

from .vectorstore import get_vectorstore

def upsert_knowledge(text: str, metadata: Optional[dict] = None, collection="iea_memory") -> None:
    """
    Insert or update a single text chunk into the vector store.
    """
    vs = get_vectorstore(collection)
    vs.add_documents([Document(page_content=text, metadata=metadata or {})])

def batch_upsert_knowledge(chunks: Iterable[str], metadata: Optional[dict] = None, collection="iea_memory") -> int:
    """
    Insert many text chunks. Returns number of added docs.
    """
    vs = get_vectorstore(collection)
    docs = [Document(page_content=txt, metadata=metadata or {}) for txt in chunks]
    if not docs:
        return 0
    vs.add_documents(docs)
    return len(docs)

def search_knowledge(query: str, k: int = 5, collection="iea_memory"):
    """
    Vector search top-k similar Documents for a query.
    """
    vs = get_vectorstore(collection)
    return vs.similarity_search(query, k=k)
