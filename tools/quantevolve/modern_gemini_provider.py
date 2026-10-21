"""Modern Google Gen AI adapter for the pinned QuantEvolve controller."""
from __future__ import annotations

import asyncio
import logging
import os
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional

from google import genai
from google.genai import types

from quantevolve.config import LLMConfig
from quantevolve.llm.base import LLMInterface

logger = logging.getLogger(__name__)
_AUDIT_LOCK = threading.Lock()


def _record_llm_event(event: str, model: str, error_type: Optional[str] = None) -> None:
    """Persist counters only; never persist prompts, response text, API keys or error messages."""
    audit_file = os.environ.get("QE_LLM_AUDIT_PATH")
    if not audit_file:
        return
    path = Path(audit_file)
    try:
        with _AUDIT_LOCK:
            data = {
                "schema_version": 1,
                "model": model,
                "requests_attempted": 0,
                "requests_succeeded": 0,
                "requests_failed": 0,
                "failure_types": {},
            }
            if path.is_file():
                try:
                    old = json.loads(path.read_text(encoding="utf-8"))
                    if isinstance(old, dict) and old.get("schema_version") == 1:
                        data.update({k: old.get(k, v) for k, v in data.items()})
                except Exception:
                    pass
            data["model"] = model
            if event == "attempt":
                data["requests_attempted"] += 1
            elif event == "success":
                data["requests_succeeded"] += 1
            elif event == "failure":
                data["requests_failed"] += 1
                failures = data.setdefault("failure_types", {})
                failures[error_type or "UnknownError"] = int(failures.get(error_type or "UnknownError", 0)) + 1
            path.parent.mkdir(parents=True, exist_ok=True)
            temp = path.with_suffix(path.suffix + ".tmp")
            temp.write_text(json.dumps(data, sort_keys=True) + "\\n", encoding="utf-8")
            temp.replace(path)
    except Exception as exc:
        # Only the exception class is logged, never the provider error string.
        logger.warning("LLM telemetry write failed (%s)", type(exc).__name__)


class GeminiLLM(LLMInterface):
    """QuantEvolve-compatible wrapper around the google-genai SDK."""

    def __init__(self, config: LLMConfig, model: Optional[str] = None):
        self.config = config
        self.model_name = model or config.primary_model
        api_key = config.api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Google Gen AI API key is not configured")
        self.client = genai.Client(api_key=api_key)

    async def generate(self, prompt: str, **kwargs) -> str:
        return await self.generate_with_context(
            system_message="", messages=[{"role": "user", "content": prompt}], **kwargs
        )

    async def generate_with_context(
        self, system_message: str, messages: List[Dict[str, str]], **kwargs
    ) -> str:
        transcript = []
        if system_message and system_message.strip():
            transcript.append("SYSTEM INSTRUCTIONS:\n" + system_message.strip())
        for message in messages:
            role = "ASSISTANT" if message.get("role") == "assistant" else "USER"
            transcript.append(role + ":\n" + str(message.get("content", "")))
        prompt = "\n\n".join(transcript)
        generation_config = types.GenerateContentConfig(
            temperature=float(kwargs.get("temperature", self.config.temperature)),
            top_p=float(kwargs.get("top_p", self.config.top_p)),
            max_output_tokens=int(kwargs.get("max_tokens", self.config.max_tokens)),
        )
        timeout_seconds = float(kwargs.get("timeout", self.config.timeout))
        _record_llm_event("attempt", self.model_name)
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model_name,
                    contents=prompt,
                    config=generation_config,
                ),
                timeout=timeout_seconds,
            )
            text = getattr(response, "text", None)
            if not isinstance(text, str) or not text.strip():
                raise RuntimeError("empty response")
            _record_llm_event("success", self.model_name)
            return text
        except Exception as exc:
            _record_llm_event("failure", self.model_name, type(exc).__name__)
            logger.error("Google Gen AI request failed (%s)", type(exc).__name__)
            raise RuntimeError("Google Gen AI request failed; details redacted") from None
