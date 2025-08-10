"""
Environment loader convenience.

We load `.env` as early as possible to ensure all modules see the
environment variables (OpenAI, Tavily, PGVector, etc.) with minimal friction.
"""
from __future__ import annotations
from pathlib import Path
from dotenv import load_dotenv

# Attempt to load from project root if present

ROOT = Path(__file__).resolve().parents[2]
env_path = ROOT / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
