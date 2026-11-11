"""Knowledge endpoint tests. No Voyage calls, no Anthropic calls, no network."""

from fastapi.testclient import TestClient

import knowledge_store as knowledge   # the SAME module the router uses
import llm
from main import app

client = TestClient(app)

STRONG_HIT = {"id": "doc-008", "title": "Benchmarking Methodology",
              "text": "Revenue per lawyer is calculated as...", "score": 0.81}
WEAK_HIT = {"id": "doc-003", "title": "Okonkwo Bell Strategy Briefing",
            "text": "Okonkwo Bell is a boutique...", "score": 0.12}
FAKE_ANSWER = {"answer": "Revenue divided by fee-earners [doc-008].",
               "input_tokens": 400, "output_tokens": 30, "stop_reason": "end_turn"}


def test_search_returns_ranked_hits(monkeypatch):
    monkeypatch.setattr(knowledge, "search", lambda q, k=3: [STRONG_HIT])

    response = client.post("/knowledge/search", json={"question": "how is PEP worked out"})
    assert response.status_code == 200
    assert response.json()["results"][0]["id"] == "doc-008"


def test_search_before_indexing_is_409(monkeypatch):
    def not_built(q, k=3):
        raise RuntimeError("Index is empty, call build_index() first")

    monkeypatch.setattr(knowledge, "search", not_built)

    response = client.post("/knowledge/search", json={"question": "anything at all"})
    assert response.status_code == 409


def test_ask_answers_and_cites_sources(monkeypatch):
    monkeypatch.setattr(knowledge, "search", lambda q, k=3: [STRONG_HIT])
    monkeypatch.setattr(llm, "answer_from_context", lambda q, c: FAKE_ANSWER)

    body = client.post("/knowledge/ask", json={"question": "how is PEP worked out"}).json()
    assert body["refused"] is False
    assert body["sources"][0]["id"] == "doc-008"
    assert body["input_tokens"] == 400


def test_ask_refuses_without_calling_the_model(monkeypatch):
    monkeypatch.setattr(knowledge, "search", lambda q, k=3: [WEAK_HIT])

    def must_not_be_called(q, c):
        raise AssertionError("The model was called despite no relevant context")

    monkeypatch.setattr(llm, "answer_from_context", must_not_be_called)

    body = client.post("/knowledge/ask", json={"question": "what is the capital of France"}).json()
    assert body["refused"] is True
    assert body["answer"] is None
    assert body["sources"] == []


def test_short_question_is_rejected_before_any_work():
    assert client.post("/knowledge/ask", json={"question": "hi"}).status_code == 422


def test_top_k_is_bounded():
    response = client.post("/knowledge/search", json={"question": "valid question", "top_k": 99})
    assert response.status_code == 422


def test_ask_reports_a_citation_to_a_source_it_never_retrieved(monkeypatch):
    drifting = {**FAKE_ANSWER, "answer": "Revenue divided by fee-earners [doc-003]."}
    monkeypatch.setattr(knowledge, "search", lambda q, k=3: [STRONG_HIT])
    monkeypatch.setattr(llm, "answer_from_context", lambda q, c: drifting)

    body = client.post("/knowledge/ask", json={"question": "how is PEP worked out"}).json()
    assert body["grounding"]["passed"] is False
    assert body["grounding"]["invalid"] == ["doc-003"]