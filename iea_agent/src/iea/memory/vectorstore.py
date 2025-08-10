from __future__ import annotations
from typing import Optional
from langchain_postgres import PGVector
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from ..config import SETTINGS

def _embeddings():
    return OpenAIEmbeddings(openai_api_key=SETTINGS.openai_api_key)

def get_vectorstore(collection: str = "iea_memory"):
    """
    Preferred vector store: PGVector (Postgres with pgvector extension).
    Fallback: Chroma persistent store under CHROMA_PERSIST_DIR.
    """
    embed = _embeddings()
    if SETTINGS.pgvector_url:
        return PGVector(
            connection=SETTINGS.pgvector_url,
            collection_name=collection,
            embeddings=embed,
        )
    return Chroma(collection_name=collection, embedding_function=embed, persist_directory=SETTINGS.chroma_dir)
