import anthropic
from fastapi.testclient import TestClient

import llm
from main import app

client = TestClient(app)

FAKE_SUMMARY = {
    "id": 1, "name": "Harding & Voss", "summary": "A fixture company",
     "input_tokens": 120, "output_tokens": 95, "stop_reason": "end_turn"
}

# tests
# what paths could the call take?

def test_summary_returns_text_and_usage(monkeypatch):
    monkeypatch.setattr(llm, "summarise_firm", lambda firm: FAKE_SUMMARY)
    response = client.post("/firms/1/summary")
    # assert what it should do
    assert response.status_code == 200
    assert response.json()["input_tokens"] == 120

def test_provider_timeout_becomes_504(monkeypatch):
    def boom(firm):
        raise anthropic.APITimeoutError(request=None)
    monkeypatch.setattr(llm, "summarise_firm", boom)
    response = client.post("/firms/1/summary")
    assert response.status_code == 504




# check that our estimate does not call the model
def test_estimate_does_not_call_the_model(monkeypatch):
    monkeypatch.setattr(llm, "estimate_input_tokens", lambda firm: 137)
    response = client.get("/firms/1/summary/estimate")

    # assertions
    assert response.status_code == 200
    assert response.json()["estimated_input_tokens"] == 137


def test_stream_yields_chunks(monkeypatch):
    monkeypatch.setattr(llm, "stream_firm_summary", lambda firm: iter(["Hard", "ing ", "& Voss"]))
    with client.stream("GET", "/firms/1/summary/stream") as response:
        assert response.status_code == 200
        body = "".join(response.iter_text())
    assert body == "Harding & Voss"