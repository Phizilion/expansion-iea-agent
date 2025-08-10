from __future__ import annotations
from dataclasses import dataclass
import os

@dataclass
class Settings:
    """
    Runtime configuration, resolved from environment variables.
    """
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-5")

    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")

    pgvector_url: str = os.getenv("PGVECTOR_URL", "")
    chroma_dir: str = os.getenv("CHROMA_PERSIST_DIR", "/data/chroma")

    log_level: str = os.getenv("IEA_LOG_LEVEL", "INFO")
    checkpoint_db: str = os.getenv("IEA_CHECKPOINT_DB", "./data/graph_checkpoints.sqlite")

# Export a singleton for convenience

SETTINGS = Settings()
