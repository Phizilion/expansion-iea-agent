"""Vector store utilities with safe fallbacks.

The original project uses external services such as Postgres/pgvector and
Chroma for persistence along with OpenAI embeddings.  Those dependencies are
heavy and optional for the unit tests in this kata, so this module now tries to
use them only when available and otherwise falls back to a very small
in‑memory store that performs a naive substring search.

The goal is to provide a deterministic, dependency free backend so the
``upsert_knowledge`` and ``search_knowledge`` helpers work out of the box.
"""

from __future__ import annotations

from typing import Dict, List

try:  # pragma: no cover - dependency may be absent
    from langchain_core.documents import Document  # type: ignore
except Exception:  # pragma: no cover - provide minimal stand-in
    from dataclasses import dataclass

    @dataclass
    class Document:  # type: ignore
        page_content: str
        metadata: dict | None = None

from ..config import SETTINGS

# Optional imports: pgvector / chroma / embeddings ---------------------------
try:  # pragma: no cover - optional dependency
    from langchain_postgres import PGVector  # type: ignore
except Exception:  # pragma: no cover - module may not be installed
    PGVector = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from langchain_community.vectorstores import Chroma  # type: ignore
except Exception:  # pragma: no cover - chromadb not installed
    Chroma = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from langchain_community.embeddings import OpenAIEmbeddings, FakeEmbeddings  # type: ignore
except Exception:  # pragma: no cover - embeddings package missing
    OpenAIEmbeddings = FakeEmbeddings = None  # type: ignore


def _embeddings():
    """Return an embedding function.

    We prefer real OpenAI embeddings when an API key is configured, otherwise a
    fast deterministic ``FakeEmbeddings`` implementation is used.  The fake
    embeddings allow similarity search to work locally without network access.
    """

    if SETTINGS.openai_api_key and OpenAIEmbeddings is not None:
        return OpenAIEmbeddings(openai_api_key=SETTINGS.openai_api_key)
    if FakeEmbeddings is not None:
        return FakeEmbeddings(size=256)
    raise RuntimeError("No embedding implementation available")


# Simple in-memory fallback store -------------------------------------------
_MEMORY: Dict[str, List[Document]] = {}


class _SimpleVectorStore:
    """Very small in-memory store used as a last resort.

    Documents are kept in a list and queries perform a case-insensitive
    substring check.  This is sufficient for the unit tests which insert and
    search for short strings.
    """

    def __init__(self, collection: str):
        self.collection = collection
        _MEMORY.setdefault(collection, [])

    def add_documents(self, docs: List[Document]) -> None:
        _MEMORY[self.collection].extend(docs)

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        docs = _MEMORY.get(self.collection, [])
        q = query.lower()
        matches = [d for d in docs if q in d.page_content.lower()]
        return matches[:k]


# Public factory -------------------------------------------------------------
def get_vectorstore(collection: str = "iea_memory"):
    """Return a vector store instance.

    Preference order:
    1. PGVector if ``langchain_postgres`` and ``psycopg`` are available and a
       ``PGVECTOR_URL`` is configured.
    2. Chroma if installed.
    3. Internal in-memory store.
    """

    # Try PGVector ----------------------------------------------------------
    if PGVector is not None and SETTINGS.pgvector_url:
        try:  # pragma: no cover - requires external service
            return PGVector(
                connection=SETTINGS.pgvector_url,
                collection_name=collection,
                embeddings=_embeddings(),
            )
        except Exception:
            pass

    # Try Chroma ------------------------------------------------------------
    if Chroma is not None:
        try:  # pragma: no cover - requires chromadb dependency
            return Chroma(
                collection_name=collection,
                embedding_function=_embeddings(),
                persist_directory=SETTINGS.chroma_dir,
            )
        except Exception:
            pass

    # Fall back to simple store --------------------------------------------
    return _SimpleVectorStore(collection)


__all__ = ["get_vectorstore"]

