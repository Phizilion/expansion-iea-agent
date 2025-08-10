from __future__ import annotations
from langchain_openai import ChatOpenAI
from config import SETTINGS

def make_llm(purpose: str = "default") -> ChatOpenAI:
    """
    Construct a `ChatOpenAI` client via langchain-openai.

    Behavior:
    - Defaults to OpenAI official endpoint.
    - If OPENROUTER_API_KEY is present, switch to OpenRouter (OpenAI-compatible schema).
    - Temperature is tuned by `purpose` (e.g., 'plan', 'execute', 'code', 'research').

    Returns:
        ChatOpenAI instance ready for tool binding.
    """
    base_url = SETTINGS.openai_base_url
    api_key = SETTINGS.openai_api_key
    model = SETTINGS.openai_model

    if SETTINGS.openrouter_api_key:
        base_url = SETTINGS.openrouter_base_url
        api_key = SETTINGS.openrouter_api_key
        model = SETTINGS.openrouter_model

    temperature = 0.1 if purpose in {"plan","code"} else 0.2

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=None,  # let server decide; tune if you prefer hard caps
    )
