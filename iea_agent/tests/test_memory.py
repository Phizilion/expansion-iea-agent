from iea.memory import upsert_knowledge, search_knowledge

def test_memory_roundtrip():
    upsert_knowledge("IEA remembers carrots are orange.", {"tag": "test"})
    hits = search_knowledge("carrots")
    assert any("carrots are orange" in d.page_content for d in hits)
