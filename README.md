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

## Why EchoLM?

EchoLM is the only language model with a **0% hallucination rate** — guaranteed by design.
