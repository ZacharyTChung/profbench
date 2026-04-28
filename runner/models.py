"""Model API wrappers used by the eval runner.

Defines a small ``ModelClient`` protocol and concrete ``ClaudeClient`` /
``GPT4oClient`` implementations. Both load API keys from the environment
(via ``python-dotenv``) and retry transient/rate-limit errors with
exponential backoff.

Adding a new model = subclass ``ModelClient`` and register it in
``MODEL_REGISTRY``.
"""

from __future__ import annotations

import os
import random
import sys
import time
from dataclasses import dataclass
from typing import Callable, Dict, Type

from dotenv import load_dotenv

load_dotenv()


SYSTEM_PROMPT = (
    "You are a professional assistant. Answer the following question as a "
    "domain expert would. Be precise and complete. Show your reasoning."
)


@dataclass
class ModelResponse:
    response: str
    tokens: int
    latency_ms: int

    def to_dict(self) -> dict:
        return {
            "response": self.response,
            "tokens": self.tokens,
            "latency_ms": self.latency_ms,
        }


def _retry(call: Callable[[], ModelResponse], *, max_attempts: int = 3) -> ModelResponse:
    """Run ``call`` with exponential backoff (0.5s, 1s, 2s + jitter)."""
    last_exc: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return call()
        except Exception as exc:  # noqa: BLE001 - retry on any API error
            last_exc = exc
            if attempt == max_attempts - 1:
                break
            sleep_for = (0.5 * (2 ** attempt)) + random.uniform(0, 0.25)
            print(
                f"[models] attempt {attempt + 1} failed: {exc!r}; "
                f"retrying in {sleep_for:.2f}s",
                file=sys.stderr,
            )
            time.sleep(sleep_for)
    assert last_exc is not None
    raise last_exc


class ModelClient:
    """Abstract base — concrete subclasses must implement ``complete``."""

    name: str = "abstract"

    def complete(self, question: str, context: str = "") -> dict:
        raise NotImplementedError


def _build_user_message(question: str, context: str) -> str:
    if context and context.strip():
        return f"# Context\n{context}\n\n# Question\n{question}"
    return question


class ClaudeClient(ModelClient):
    """Anthropic Claude wrapper."""

    name = "claude-sonnet-4-6"

    def __init__(self, model: str | None = None, max_tokens: int = 2048) -> None:
        from anthropic import Anthropic  # imported lazily so dry-run works without the SDK

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in."
            )
        self.client = Anthropic(api_key=api_key)
        self.model = model or self.name
        self.max_tokens = max_tokens

    def complete(self, question: str, context: str = "") -> dict:
        def _do() -> ModelResponse:
            t0 = time.perf_counter()
            msg = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": _build_user_message(question, context)}],
            )
            elapsed_ms = int((time.perf_counter() - t0) * 1000)
            text = "".join(
                block.text for block in msg.content if getattr(block, "type", None) == "text"
            )
            tokens = (msg.usage.input_tokens + msg.usage.output_tokens) if msg.usage else 0
            return ModelResponse(response=text, tokens=tokens, latency_ms=elapsed_ms)

        return _retry(_do).to_dict()


class OpusClient(ClaudeClient):
    """Anthropic Claude Opus 4.7 — strongest, most expensive."""

    name = "claude-opus-4-7"


class HaikuClient(ClaudeClient):
    """Anthropic Claude Haiku 4.5 — smallest, cheapest."""

    name = "claude-haiku-4-5"


class GPT4oClient(ModelClient):
    """OpenAI GPT-4o wrapper."""

    name = "gpt-4o"

    def __init__(self, model: str | None = None, max_tokens: int = 2048) -> None:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy .env.example to .env and fill it in."
            )
        self.client = OpenAI(api_key=api_key)
        self.model = model or self.name
        self.max_tokens = max_tokens

    def complete(self, question: str, context: str = "") -> dict:
        def _do() -> ModelResponse:
            t0 = time.perf_counter()
            resp = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": _build_user_message(question, context)},
                ],
            )
            elapsed_ms = int((time.perf_counter() - t0) * 1000)
            text = resp.choices[0].message.content or ""
            tokens = resp.usage.total_tokens if resp.usage else 0
            return ModelResponse(response=text, tokens=tokens, latency_ms=elapsed_ms)

        return _retry(_do).to_dict()


MODEL_REGISTRY: Dict[str, Type[ModelClient]] = {
    "claude": ClaudeClient,   # Sonnet 4.6
    "sonnet": ClaudeClient,   # explicit alias
    "opus": OpusClient,       # Opus 4.7
    "haiku": HaikuClient,     # Haiku 4.5
    "gpt4o": GPT4oClient,
}


def build_client(alias: str) -> ModelClient:
    """Instantiate a model client by short alias (e.g. ``claude``, ``gpt4o``)."""
    alias = alias.strip().lower()
    if alias not in MODEL_REGISTRY:
        raise ValueError(
            f"Unknown model alias '{alias}'. Known: {sorted(MODEL_REGISTRY)}"
        )
    return MODEL_REGISTRY[alias]()
