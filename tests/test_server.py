"""Tests for the OpenAI-compatible HTTP server."""

import json
import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from echolm.server import app

client = TestClient(app)


class TestModelsEndpoint:
    def test_lists_echolm_model(self):
        response = client.get("/v1/models")
        assert response.status_code == 200
        data = response.json()
        assert data["object"] == "list"
        ids = [m["id"] for m in data["data"]]
        assert "echolm" in ids


class TestChatCompletions:
    def _post(self, messages, stream=False, **kwargs):
        payload = {"model": "echolm", "messages": messages, "stream": stream, **kwargs}
        return client.post("/v1/chat/completions", json=payload)

    def test_echoes_last_user_message(self):
        response = self._post([{"role": "user", "content": "Hello!"}])
        assert response.status_code == 200
        data = response.json()
        assert data["choices"][0]["message"]["content"] == "Hello!"
        assert data["choices"][0]["message"]["role"] == "assistant"
        assert data["choices"][0]["finish_reason"] == "stop"

    def test_echoes_last_user_message_in_multi_turn(self):
        messages = [
            {"role": "user", "content": "first"},
            {"role": "assistant", "content": "first"},
            {"role": "user", "content": "second"},
        ]
        response = self._post(messages)
        assert response.status_code == 200
        assert response.json()["choices"][0]["message"]["content"] == "second"

    def test_empty_content_when_no_user_message(self):
        response = self._post([{"role": "system", "content": "You are helpful."}])
        assert response.status_code == 200
        assert response.json()["choices"][0]["message"]["content"] == ""

    def test_response_structure(self):
        response = self._post([{"role": "user", "content": "hi"}])
        data = response.json()
        assert "id" in data
        assert "created" in data
        assert data["object"] == "chat.completion"
        assert data["model"] == "echolm"
        assert "usage" in data

    def test_accepts_optional_fields(self):
        response = self._post(
            [{"role": "user", "content": "hi"}],
            temperature=0.7,
            max_tokens=100,
            top_p=1.0,
        )
        assert response.status_code == 200

    def test_streaming_response(self):
        with client.stream(
            "POST",
            "/v1/chat/completions",
            json={"model": "echolm", "messages": [{"role": "user", "content": "ping"}], "stream": True},
        ) as response:
            assert response.status_code == 200
            assert "text/event-stream" in response.headers["content-type"]
            raw = response.read().decode()

        lines = [l for l in raw.splitlines() if l.startswith("data: ")]
        assert lines[-1] == "data: [DONE]"

        # Collect delta content from chunks
        content = ""
        for line in lines[:-1]:
            chunk = json.loads(line[len("data: "):])
            delta = chunk["choices"][0]["delta"]
            content += delta.get("content", "")

        assert content == "ping"

    def test_streaming_finish_reason(self):
        with client.stream(
            "POST",
            "/v1/chat/completions",
            json={"model": "echolm", "messages": [{"role": "user", "content": "x"}], "stream": True},
        ) as response:
            raw = response.read().decode()

        lines = [l for l in raw.splitlines() if l.startswith("data: ") and l != "data: [DONE]"]
        last_chunk = json.loads(lines[-1][len("data: "):])
        assert last_chunk["choices"][0]["finish_reason"] == "stop"
