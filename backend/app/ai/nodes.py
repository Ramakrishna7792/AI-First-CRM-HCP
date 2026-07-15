"""
LangGraph Nodes

These nodes are responsible for:

1. Intent Detection
2. Entity Extraction
3. Validation
4. Response Generation

The actual database work is handled by the LangGraph tools.
"""

import json
import logging

from app.ai.prompts import SYSTEM_PROMPT
from app.ai.state import InteractionGraphState
from app.core.config import settings

logger = logging.getLogger(__name__)

# ChatGroq is instantiated lazily to avoid crash when GROQ_API_KEY is absent.
_llm = None


def _get_llm():
    """Return a cached ChatGroq instance, creating it on first call."""
    global _llm
    if _llm is None:
        from langchain_groq import ChatGroq
        _llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0,
        )
    return _llm


# ----------------------------------------------------------
# Intent Detection
# ----------------------------------------------------------


def detect_intent(state: InteractionGraphState) -> dict:
    if not settings.groq_api_key:
        logger.debug("detect_intent: no API key, defaulting to 'log'")
        return {**state, "intent": "log"}

    prompt = f"""You are an AI CRM assistant.

Determine the user's intent.

Return ONLY one of these values.

log

edit

summary

followup

compliance

User Message

{state["message"]}
"""

    response = _get_llm().invoke(prompt)
    intent = response.content.strip().lower()

    allowed = {"log", "edit", "summary", "followup", "compliance"}
    if intent not in allowed:
        intent = "log"

    return {**state, "intent": intent}


# ----------------------------------------------------------
# Entity Extraction
# ----------------------------------------------------------


def extract_entities(state: InteractionGraphState) -> dict:
    if not settings.groq_api_key:
        logger.debug("extract_entities: no API key, returning empty extracted")
        return {**state, "extracted": {}}

    prompt = SYSTEM_PROMPT.format(message=state["message"])
    response = _get_llm().invoke(prompt)

    try:
        extracted = json.loads(response.content)
    except Exception:
        extracted = {}

    return {**state, "extracted": extracted}


# ----------------------------------------------------------
# Validation
# ----------------------------------------------------------


REQUIRED_FIELDS = [
    "doctor_name",
    "interaction_type",
]


def validate_interaction(state: InteractionGraphState) -> dict:
    data = state.get("merged_draft") or state.get("extracted") or {}

    missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
    warnings = ["Some required fields are missing."] if missing else []

    return {**state, "missing_fields": missing, "warnings": warnings}


# ----------------------------------------------------------
# Assistant Response
# ----------------------------------------------------------


def build_response(state: InteractionGraphState) -> dict:
    missing = state.get("missing_fields", [])

    if missing:
        reply = (
            "Interaction analyzed successfully.\n\n"
            "Please complete the missing fields:\n\n"
            + "\n".join(f"• {item}" for item in missing)
        )
    else:
        reply = "Interaction processed successfully."

    return {**state, "reply": reply}