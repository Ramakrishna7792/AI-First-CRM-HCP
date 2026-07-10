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

from langchain_groq import ChatGroq

from app.ai.prompts import SYSTEM_PROMPT
from app.core.config import settings

llm = ChatGroq(
    api_key=settings.groq_api_key,
    model=settings.groq_model,
    temperature=0,
)


# ----------------------------------------------------------
# Intent Detection
# ----------------------------------------------------------


def detect_intent(state):

    prompt = f"""
You are an AI CRM assistant.

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

    response = llm.invoke(prompt)

    intent = response.content.strip().lower()

    allowed = {
        "log",
        "edit",
        "summary",
        "followup",
        "compliance",
    }

    if intent not in allowed:
        intent = "log"

    return {
        **state,
        "intent": intent,
    }


# ----------------------------------------------------------
# Entity Extraction
# ----------------------------------------------------------


def extract_entities(state):

    prompt = SYSTEM_PROMPT.format(
        message=state["message"]
    )

    response = llm.invoke(prompt)

    try:

        extracted = json.loads(response.content)

    except Exception:

        extracted = {}

    return {
        **state,
        "extracted": extracted,
    }


# ----------------------------------------------------------
# Validation
# ----------------------------------------------------------


REQUIRED_FIELDS = [
    "doctor_name",
    "interaction_type",
]


def validate_interaction(state):

    data = state.get("merged_draft") or state.get("extracted") or {}

    missing = []

    for field in REQUIRED_FIELDS:

        if not data.get(field):

            missing.append(field)

    warnings = []

    if missing:

        warnings.append(
            "Some required fields are missing."
        )

    return {
        **state,
        "missing_fields": missing,
        "warnings": warnings,
    }


# ----------------------------------------------------------
# Assistant Response
# ----------------------------------------------------------


def build_response(state):

    missing = state.get("missing_fields", [])

    if missing:

        reply = (
            "Interaction analyzed successfully.\n\n"
            "Please complete the missing fields:\n\n"
            + "\n".join(
                f"• {item}" for item in missing
            )
        )

    else:

        reply = (
            "Interaction processed successfully."
        )

    return {
        **state,
        "reply": reply,
    }