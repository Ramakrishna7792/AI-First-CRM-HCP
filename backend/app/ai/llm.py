"""
Shared Groq LLM client.

This module provides a singleton wrapper around the Groq client used by
the AI Agent, LangGraph nodes, and AI tools.

Responsibilities
----------------
- Initialize Groq only once.
- Expose async chat completion methods.
- Centralize model configuration.
- Handle retries and API failures.
- Return structured responses.

Author:
AI-First CRM Interview Assignment
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from groq import APIConnectionError, APIStatusError, AsyncGroq, RateLimitError

from app.core.config import settings

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemma2-9b-it"


class LLMException(Exception):
    """Raised when the LLM cannot generate a response."""


class GroqLLM:
    """
    Singleton wrapper around Groq.

    Example
    -------
    llm = GroqLLM()

    result = await llm.chat(
        system_prompt="...",
        user_prompt="..."
    )
    """

    _instance: Optional["GroqLLM"] = None

    def __new__(cls) -> "GroqLLM":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized"):
            return

        self.client = AsyncGroq(api_key=settings.groq_api_key)
        self.model = settings.groq_model or DEFAULT_MODEL
        self.max_retries = 3
        self.temperature = 0.2
        self.timeout = 60
        self._initialized = True

        logger.info("Groq LLM initialized with model=%s", self.model)

    async def _create_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float | None = None,
        max_tokens: int = 1024,
    ) -> str:
        """Low-level Groq API call with retries."""
        retries = 0

        while retries < self.max_retries:
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature if temperature is not None else self.temperature,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content.strip()

            except RateLimitError:
                retries += 1
                wait = retries * 2
                logger.warning("Groq rate limit. Retrying in %s sec", wait)
                await asyncio.sleep(wait)

            except APIConnectionError as exc:
                logger.exception(exc)
                raise LLMException("Unable to connect to Groq.") from exc

            except APIStatusError as exc:
                logger.exception(exc)
                raise LLMException(f"Groq returned status {exc.status_code}") from exc

            except Exception as exc:
                logger.exception(exc)
                raise LLMException("Unexpected LLM failure.") from exc

        raise LLMException("Maximum retry attempts exceeded.")

    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float | None = None,
        max_tokens: int = 1024,
    ) -> str:
        """Generate a standard chat completion."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return await self._create_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def json_chat(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_hint: str | None = None,
    ) -> Dict[str, Any]:
        """
        Ask the model to return JSON only.

        Returns
        -------
        dict
        """
        prompt = user_prompt
        if schema_hint:
            prompt += f"\n\nReturn ONLY valid JSON.\n\nSchema:\n{schema_hint}"

        response = await self.chat(
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=0.1,
        )
        return self.parse_json(response)

    async def summarize(self, text: str) -> str:
        """Summarize interaction history."""
        system_prompt = (
            "You are a Healthcare CRM assistant.\n"
            "Generate concise interaction summaries.\n"
            "Focus on: doctor, products, concerns, commitments, outcome, next follow-up."
        )
        return await self.chat(system_prompt=system_prompt, user_prompt=text, temperature=0.2)

    async def compliance_check(self, interaction_text: str) -> Dict[str, Any]:
        """Detect compliance issues."""
        system_prompt = (
            "You are a pharmaceutical compliance officer.\n"
            "Check for: prohibited medical claims, misleading efficacy, "
            "unsupported statements, missing mandatory information.\n"
            'Return JSON. Example: {"status":"PASS","warnings":[]}'
        )
        return await self.json_chat(system_prompt=system_prompt, user_prompt=interaction_text)

    async def followup_recommendation(self, context: str) -> str:
        """Generate HCP follow-up recommendations."""
        system_prompt = (
            "You are an experienced Medical Representative coach.\n"
            "Suggest: follow-up priority, samples, brochures, discussion points, visit interval.\n"
            "Keep recommendations practical."
        )
        return await self.chat(
            system_prompt=system_prompt, user_prompt=context, temperature=0.3
        )

    async def extract_entities(self, interaction: str) -> Dict[str, Any]:
        """Convert free text into structured interaction data."""
        schema = (
            '{"doctor_name":"","hospital":"","products":[],'
            '"discussion":"","outcome":"","sentiment":"","next_followup":""}'
        )
        system_prompt = "You extract structured CRM interaction information.\nReturn ONLY JSON."
        return await self.json_chat(
            system_prompt=system_prompt,
            user_prompt=interaction,
            schema_hint=schema,
        )

    @staticmethod
    def parse_json(text: str) -> Dict[str, Any]:
        """Safely parse JSON returned by the LLM."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())

    async def generate_title(self, interaction_text: str) -> str:
        """Generate a short title for an interaction."""
        system_prompt = (
            "Generate a concise CRM interaction title.\n"
            "Examples: Cardiology Visit, Product Follow-up, Diabetes Consultation\n"
            "Return only the title."
        )
        return await self.chat(
            system_prompt=system_prompt,
            user_prompt=interaction_text,
            temperature=0.2,
            max_tokens=32,
        )

    async def classify_intent(self, message: str) -> Dict[str, Any]:
        """
        Predict the intent for LangGraph routing.

        Supported intents: log, edit, summary, followup, compliance, pdf
        """
        schema = '{"intent":"","confidence":0.0}'
        system_prompt = (
            "You are an Intent Classifier.\n"
            "Choose exactly one intent.\n"
            "Allowed values: log, edit, summary, followup, compliance, pdf\n"
            "Return ONLY JSON."
        )
        return await self.json_chat(
            system_prompt=system_prompt,
            user_prompt=message,
            schema_hint=schema,
        )

    async def health_check(self) -> bool:
        """Verify that the configured Groq model is reachable."""
        try:
            await self.chat(
                system_prompt="Reply with OK.",
                user_prompt="health",
                max_tokens=8,
            )
            return True
        except Exception:
            logger.exception("Groq health check failed.")
            return False

    async def close(self) -> None:
        """Placeholder for future cleanup."""
        return None


# ------------------------------------------------------------------
# Shared singleton — lazy to avoid crash when API key is absent
# ------------------------------------------------------------------

_llm_instance: GroqLLM | None = None


def get_llm() -> GroqLLM:
    """Returns the shared GroqLLM singleton. Created on first call."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = GroqLLM()
    return _llm_instance


__all__ = ["GroqLLM", "LLMException", "get_llm"]