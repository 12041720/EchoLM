"""OpenAI-compatible HTTP server for EchoLM."""

import json
import time
import uuid
from typing import Iterator, List, Optional, Union

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse
    from pydantic import BaseModel
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "Server dependencies are not installed. "
        "Run: pip install 'echolm[server]'"
    ) from exc

from echolm.model import EchoLM

app = FastAPI(title="EchoLM", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_model = EchoLM()
_MODEL_ID = "echolm"


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = _MODEL_ID
    messages: List[Message]
    stream: bool = False
    # Accept (and ignore) common optional fields so clients don't get errors.
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _last_user_content(messages: List[Message]) -> str:
    """Return the content of the last user message, or "" if none."""
    for msg in reversed(messages):
        if msg.role == "user":
            return msg.content
    return ""


def _make_chunk(chunk_id: str, created: int, delta: dict, finish_reason: Optional[str]) -> str:
    payload = {
        "id": chunk_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": _MODEL_ID,
        "choices": [
            {
                "index": 0,
                "delta": delta,
                "finish_reason": finish_reason,
            }
        ],
    }
    return f"data: {json.dumps(payload)}\n\n"


def _stream_response(reply: str, chunk_id: str, created: int) -> Iterator[str]:
    # First chunk: role
    yield _make_chunk(chunk_id, created, {"role": "assistant", "content": ""}, None)
    # Content chunk
    yield _make_chunk(chunk_id, created, {"content": reply}, None)
    # Final chunk
    yield _make_chunk(chunk_id, created, {}, "stop")
    yield "data: [DONE]\n\n"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/v1/models")
def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": _MODEL_ID,
                "object": "model",
                "created": 0,
                "owned_by": "echolm",
            }
        ],
    }


@app.post("/v1/chat/completions")
def chat_completions(request: ChatCompletionRequest):
    reply = _model.generate(_last_user_content(request.messages))
    chunk_id = f"chatcmpl-{uuid.uuid4().hex}"
    created = int(time.time())

    if request.stream:
        return StreamingResponse(
            _stream_response(reply, chunk_id, created),
            media_type="text/event-stream",
        )

    return {
        "id": chunk_id,
        "object": "chat.completion",
        "created": created,
        "model": _MODEL_ID,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": reply},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


# ---------------------------------------------------------------------------
# Entry point (used by the CLI)
# ---------------------------------------------------------------------------

def serve(host: str = "127.0.0.1", port: int = 8000) -> None:  # pragma: no cover
    """Start the uvicorn server."""
    try:
        import uvicorn
    except ImportError as exc:
        raise ImportError(
            "Server dependencies are not installed. "
            "Run: pip install 'echolm[server]'"
        ) from exc

    uvicorn.run(app, host=host, port=port)
