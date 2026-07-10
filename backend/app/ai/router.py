"""
router.py

LangGraph Router

This router decides which tool should execute
based on the detected user intent.
"""

from app.ai.state import InteractionGraphState


VALID_INTENTS = {
    "log",
    "edit",
    "summary",
    "followup",
    "compliance",
}


def route_intent(state: InteractionGraphState) -> str:
    """
    Determine which LangGraph node should run.

    Expected values:

    log
    edit
    summary
    followup
    compliance

    Any unknown value defaults to "log".
    """

    intent = (
        state.get("intent", "log")
        .strip()
        .lower()
    )

    if intent not in VALID_INTENTS:
        return "log"

    return intent


def should_validate(state: InteractionGraphState) -> str:
    """
    Decide whether validation should run.

    Only log/edit interactions require
    CRM field validation.
    """

    intent = state.get("intent", "").lower()

    if intent in {"log", "edit"}:
        return "validate"

    return "response"


def should_save(state: InteractionGraphState) -> str:
    """
    Decide whether interaction should be
    persisted into PostgreSQL.

    Summary / Follow-up / Compliance
    never save data.
    """

    intent = state.get("intent", "").lower()

    if intent in {"log", "edit"}:
        return "save"

    return "response"