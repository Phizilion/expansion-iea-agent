# IEA-PoC (Independent Economic Activity) — LangGraph POC

This proof-of-concept shows a self-improving agent capable of:
- **Targeting**: decide whether to execute a target now or decompose it one level.
- **Information Exploration**: internal memory → vector DB → web search → synthesis.
- **Self-Modification**: read its own code → propose a patch → test → iterate → merge + hot-reload.

## Quick Start

```bash
cp .env.example .env
# Fill OpenAI + Tavily keys, leave PGVECTOR as-is (Dockerized).

docker compose up --build
# Installs Playwright browsers, runs tests, then launches CLI.

# Run targeting on a goal:
docker compose exec app python -m iea.cli target "Find 3 micro-revenue ideas for a solo developer and produce a brief with sources."

# Run info brief directly:
docker compose exec app python -m iea.cli brief "Practical Asahi Arch + Hyprland tuning tips on M2 Max"

# Try self-modification (toy)
docker compose exec app python -m iea.cli selfmod "Refactor memory batch upserts"
```

## Design Highlights

* **LangGraph** controls agent state reliably with resume-ability.
* **GPT-5** (via `langchain-openai`) is the primary reasoning & coding model (configurable).
* **Tavily** for search; **Playwright** for browser actions.
* **PGVector** default memory; **Chroma** fallback if PG isn’t available.

## Safety & ToS

* The agent prepares artifacts but **does not** auto-submit to external platforms without a human’s explicit action.
* Self-mod pipeline applies changes within the repo and requires tests passing before merge.

---

## Repo Structure

```
src/iea/
  cli.py
  config.py
  env.py
  logging.py
  llm.py
  memory/
    __init__.py
    vectorstore.py
    knowledge_base.py
  tools/
    __init__.py
    web_search.py
    browser.py
    fs_git.py
    shell.py
    http_client.py
    parser.py
  graphs/
    __init__.py
    targeting.py
    info.py
    self_mod.py
    orchestration.py
  prompts/
    __init__.py
    system_prompts.py

tests/
  test_smoke.py
  test_memory.py
  test_tools_fs_git.py
  test_graph_targeting.py
  test_graph_selfmod.py
```

---

## Notes

* Everything runs inside Docker for consistency. If you prefer local runs, install deps, start a local Postgres with pgvector, and set `PGVECTOR_URL`.
* Edit `prompts/system_prompts.py` to tune agent personality and guardrails.
