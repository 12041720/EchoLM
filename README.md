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

Windows (cmd):

```cmd
pip install -e .
pip install -e ".[server]"
```

macOS / Linux:

```bash
pip install -e .
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

Windows (cmd):

```cmd
echolm "Hello, world!"
# Hello, world!
```

macOS / Linux:

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

This command is the same on Windows, macOS, and Linux.

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

OpenCode discovers models from its provider config. If your model does not
show up after setting environment variables, add a project-level
`opencode.json` file like this:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "echolm": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "EchoLM (local)",
      "options": {
        "baseURL": "http://127.0.0.1:8000/v1"
      },
      "models": {
        "echolm": {
          "name": "EchoLM"
        }
      }
    }
  },
  "model": "echolm/echolm"
}
```

You can still use environment variables for one-off runs, but the config file
is what makes the model appear consistently in the selector.

Windows (cmd):

```cmd
start "" echolm serve
set OPENAI_BASE_URL=http://127.0.0.1:8000/v1
set OPENAI_API_KEY=not-needed
opencode
```

macOS / Linux:

```bash
echolm serve &
export OPENAI_BASE_URL=http://127.0.0.1:8000/v1
export OPENAI_API_KEY=not-needed
opencode
```

If you prefer environment variables, keep using the same base URL and API key
values above; just note that they do not add the model to OpenCode by
themselves.

**Quick test with curl:**

Windows (cmd):

```cmd
curl.exe http://127.0.0.1:8000/v1/chat/completions ^
  -H "Content-Type: application/json" ^
  -d "{\"model\":\"echolm\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello!\"}]}"
```

macOS / Linux:

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

