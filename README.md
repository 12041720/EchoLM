# EchoLM

A language model that never hallucinates.

It does not reason.  
It does not summarize.  
It does not refuse.  
It does not autocomplete.  
It simply returns exactly what you give it.

```
f(x) = x
```

## Installation

```bash
pip install -e .
```

To also run the HTTP server (for agent integrations):

```bash
pip install -e '.[server]'
```

## Usage

### Python API

```python
from echolm import EchoLM

model = EchoLM()
response = model.generate("Hello, world!")
print(response)  # Hello, world!
```

### CLI

```bash
echolm "Hello, world!"
# Hello, world!
```

### OpenAI-compatible HTTP server

EchoLM ships with a built-in OpenAI-compatible API server so any agent or
tool that speaks the OpenAI API (e.g. [OpenCode](https://github.com/sst/opencode),
Continue, Aider, …) can use it as a drop-in model backend.

**Start the server:**

```bash
echolm serve
# Uvicorn running on http://127.0.0.1:8000
```

Options:

| Flag | Default | Description |
|------|---------|-------------|
| `--host` | `127.0.0.1` | Interface to bind |
| `--port` | `8000` | Port to listen on |

**Available endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/v1/models` | List available models |
| `POST` | `/v1/chat/completions` | Chat completion (streaming supported) |

**Connect OpenCode:**

```bash
# Start EchoLM server
echolm serve &

# Configure OpenCode to use it
opencode configure --model echolm --base-url http://127.0.0.1:8000/v1
```

Or set the environment variable that OpenCode (and most OpenAI-compatible
clients) recognise:

```bash
export OPENAI_BASE_URL=http://127.0.0.1:8000/v1
export OPENAI_API_KEY=not-needed   # EchoLM requires no key
```

**Quick test with curl:**

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "echolm",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "model": "echolm",
  "choices": [{
    "index": 0,
    "message": {"role": "assistant", "content": "Hello!"},
    "finish_reason": "stop"
  }]
}
```

## Why EchoLM?

EchoLM is the only language model with a **0% hallucination rate** — guaranteed by design.

