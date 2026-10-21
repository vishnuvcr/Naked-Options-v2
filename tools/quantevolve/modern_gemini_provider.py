"""Modern Google Gen AI adapter for the pinned QuantEvolve controller."""
from __future__ import annotations

import asyncio
import logging
import os
from typing import Dict, List, Optional

from google import genai
from google.genai import types

from quantevolve.config import LLMConfig
from quantevolve.llm.base import LLMInterface

logger = logging.getLogger(__name__)


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
            return text
        except Exception as exc:
            logger.error("Google Gen AI request failed (%s)", type(exc).__name__)
            raise RuntimeError("Google Gen AI request failed; details redacted") from None
