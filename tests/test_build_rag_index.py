"""実SQLiteと固定ベクトルで、索引作成から検索までを確認する。APIは呼ばない。"""

import json
from unittest.mock import Mock

import pytest

from app import retrieval
from scripts.build_rag_index import build_index


@pytest.fixture
def materials(tmp_path):
    source = tmp_path / "lectures.json"
    source.write_text(json.dumps([
        {"id": f"lec{n:02d}-main", "title": f"講義{n}", "content": [
            {"section": "章", "content": [
                {"id": f"lec{n:02d}-main-p001", "title": f"ページ{n}",
                 "page": 1, "content": f"本文{n}"}]}]}
        for n in (1, 2, 5)
    ], ensure_ascii=False), encoding="utf-8")
    return source, tmp_path / "index.sqlite3"


def test_built_index_can_be_searched(materials, monkeypatch):
    source, database = materials
    texts = []

    def embed(text, task):
        assert task == "RETRIEVAL_DOCUMENT"
        texts.append(text)
        return [1, 0] if "本文1" in text else [0, 1]

    result = build_index(source, database, embedder=embed)
    assert result["pages"] == 2  # 第5回の資料は検索対象に含めない
    assert all("章" in text and "ページ" in text for text in texts)
    monkeypatch.setattr(retrieval, "RAG_DB", database)
    monkeypatch.setattr(retrieval, "embed_text", lambda *_: [1, 0])
    hits = retrieval.search("質問")
    assert [h["page_id"] for h in hits] == ["lec01-main-p001", "lec02-main-p001"]
    assert hits[0]["content"] == "本文1"
    assert hits[0]["distance"] == pytest.approx(0)


def test_graph_search_traverses_related_terms_with_weights(tmp_path, monkeypatch):
    source = tmp_path / "lectures.json"
    source.write_text(json.dumps([
        {"id": "lec02-main", "title": "基盤モデル", "content": [
            {"section": "章", "content": [
                {"id": "lec02-main-p052", "title": "LoRAとQLoRA", "page": 52,
                 "content": "LoRAとQLoRAの説明"},
                {"id": "lec02-main-p053", "title": "関連するQLoRAの説明", "page": 53,
                 "content": "QLoRAは4bit量子化する"}]}
        ]}
    ], ensure_ascii=False), encoding="utf-8")
    graph = tmp_path / "graph.json"
    graph.write_text(json.dumps({
        "nodes": [
            {"id": "lec02-main-p052", "kind": "page", "title": "LoRAとQLoRA"},
            {"id": "lec02-main-p053", "kind": "page", "title": "関連するQLoRAの説明"},
            {"id": "term:lora", "kind": "term", "title": "LoRA"},
            {"id": "term:qlora", "kind": "term", "title": "QLoRA"},
        ],
        "edges": [
            {"source": "lec02-main-p052", "target": "term:lora", "relation": "mentions"},
            {"source": "term:lora", "target": "term:qlora", "relation": "related_term"},
            {"source": "term:qlora", "target": "lec02-main-p053", "relation": "mentions"},
        ],
    }, ensure_ascii=False), encoding="utf-8")

    monkeypatch.setattr(retrieval, "RAG_SOURCE", source)
    monkeypatch.setattr(retrieval, "RAG_GRAPH", graph)
    monkeypatch.setattr(retrieval, "GRAPH_HOPS", 3)
    monkeypatch.setattr(retrieval, "search", lambda query: [
        {"page_id": "lec02-main-p052", "distance": 0.1,
         "content": "LoRAとQLoRAの説明"}
    ])

    result = retrieval.search_graph("LoRAとQLoRA")

    assert result["seeds"]
    assert [candidate["page_id"] for candidate in result["expanded"]] == ["lec02-main-p053"]
    assert result["expanded"][0]["relation_weight"] == 2.3
    assert result["relation_weights"]["related_term"] == 0.7


def test_existing_index_survives_failed_rebuild(materials):
    source, database = materials
    build_index(source, database, embedder=lambda *_: [1, 0])
    before = database.read_bytes()
    embed = Mock(side_effect=RuntimeError("埋め込みに失敗"))
    with pytest.raises(FileExistsError):
        build_index(source, database, embedder=embed)
    embed.assert_not_called()
    with pytest.raises(RuntimeError, match="埋め込みに失敗"):
        build_index(source, database, rebuild=True, embedder=embed)
    assert database.read_bytes() == before
    assert not list(database.parent.glob(".rag-build-*"))
