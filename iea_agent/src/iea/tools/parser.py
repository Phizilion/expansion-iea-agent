from __future__ import annotations
from langchain_core.tools import tool
import re

@tool("extract_text", return_direct=False)
def extract_text(html: str) -> str:
    """
    Naive HTML to text extractor (regex-based). For richer parsing use BeautifulSoup if desired.
    """
    try:
        text = re.sub(r"<script.*?</script>", " ", html, flags=re.S|re.I)
        text = re.sub(r"<style.*?</style>", " ", text, flags=re.S|re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:4000]
    except Exception as e:
        return f"PARSER_ERROR: {type(e).__name__}: {e}"
