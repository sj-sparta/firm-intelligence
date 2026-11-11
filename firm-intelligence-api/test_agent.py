# 1. set up some fake building blocks
# 2. create a fake model (that keeps going)
# 3. sub in our fakes from step 1
# 4. hit our endpoint
# 5. check it stopped
# pretend the model never stops... check your code stops it anyway

from fastapi.testclient import TestClient

import agent
from main import app

client = TestClient(app)


class FakeToolUseBlock:
    type = "tool_use"
    name = "search_knowledge_base"

    def __init__(self, input_, id_="toolu_01"):
        self.input = input_
        self.id = id_


class FakeTextBlock:
    type = "text"

    def __init__(self, text):
        self.text = text


class FakeUsage:
    def __init__(self, i, o):
        self.input_tokens, self.output_tokens = i, o


class FakeResponse:
    def __init__(self, content, stop_reason, usage):
        self.content, self.stop_reason, self.usage = content, stop_reason, usage


FAKE_HIT = [{"id": "doc-001", "title": "t", "text": "x", "score": 0.5}]


def test_agent_stops_at_max_iterations_instead_of_looping_forever(monkeypatch):
    def fake_create(**kwargs):
        return FakeResponse(
            [FakeToolUseBlock({"query": "anything"})], "tool_use", FakeUsage(100, 15)
        )

    monkeypatch.setattr(agent.client.messages, "create", fake_create)
    monkeypatch.setattr(agent.knowledge, "search", lambda q, top_k=3: FAKE_HIT)

    response = client.post("/agent/ask", json={"question": "never resolves"})
    body = response.json()

    assert body["completed"] is False
    assert body["stop_reason"] == "max_iterations"
    assert body["tool_calls_made"] == agent.MAX_ITERATIONS


def test_agent_answers_two_tool_calls_made_in_one_turn(monkeypatch):
    turns = [
        FakeResponse(
            [FakeToolUseBlock({"query": "a"}, "toolu_A"),
             FakeToolUseBlock({"query": "b"}, "toolu_B")],
            "tool_use", FakeUsage(100, 20),
        ),
        FakeResponse([FakeTextBlock("Done [doc-001].")], "end_turn", FakeUsage(150, 30)),
    ]
    calls = []

    def fake_create(**kwargs):
        calls.append(list(kwargs["messages"]))
        return turns[len(calls) - 1]

    monkeypatch.setattr(agent.client.messages, "create", fake_create)
    monkeypatch.setattr(agent.knowledge, "search", lambda q, top_k=3: FAKE_HIT)

    body = client.post("/agent/ask", json={"question": "two searches"}).json()

    assert body["completed"] is True
    assert body["tool_calls_made"] == 2
    last_message_of_second_call = calls[1][-1]
    answered_ids = {block["tool_use_id"] for block in last_message_of_second_call["content"]}
    assert answered_ids == {"toolu_A", "toolu_B"}