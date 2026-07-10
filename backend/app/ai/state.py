"""
LangGraph State Definition

This state object is shared across every node in the graph.

The graph supports multiple AI tools:

1. Log Interaction
2. Edit Interaction
3. Interaction Summary
4. Follow-up Recommendation
5. Compliance Checker
"""

from typing import Any, Literal, TypedDict


class InteractionGraphState(TypedDict, total=False):
    # ------------------------------------------------------------------
    # User Input
    # ------------------------------------------------------------------

    message: str

    conversation: list[dict[str, str]]

    # ------------------------------------------------------------------
    # Intent Detection
    # ------------------------------------------------------------------

    intent: Literal[
        "log",
        "edit",
        "summary",
        "followup",
        "compliance",
    ]

    # ------------------------------------------------------------------
    # Existing CRM Draft
    # ------------------------------------------------------------------

    existing_draft: dict[str, Any]

    # ------------------------------------------------------------------
    # LLM Extraction
    # ------------------------------------------------------------------

    extracted: dict[str, Any]

    merged_draft: dict[str, Any]

    # ------------------------------------------------------------------
    # Doctor Information
    # ------------------------------------------------------------------

    doctor: dict[str, Any]

    # ------------------------------------------------------------------
    # Interaction Information
    # ------------------------------------------------------------------

    interaction: dict[str, Any]

    # ------------------------------------------------------------------
    # Tool Result
    # ------------------------------------------------------------------

    tool_output: dict[str, Any]

    # ------------------------------------------------------------------
    # Assistant Response
    # ------------------------------------------------------------------

    reply: str

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    missing_fields: list[str]

    warnings: list[str]