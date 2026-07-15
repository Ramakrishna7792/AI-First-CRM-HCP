"""
HCPCRMAgent

Main AI orchestrator for the HCP CRM system.

Architecture
------------
FastAPI → HCPCRMAgent.run()
            ↓
        detect_intent()
            ↓
    ┌───────┴────────┐
    │   Route to     │
    │   AI Tool      │
    └───────┬────────┘
            ↓
      Tool calls Service (if needed)
            ↓
        Structured response

Design decisions
----------------
- Intent detection uses fast keyword heuristics so no LLM call is needed
  for routing. This keeps latency low and avoids circular API dependencies.
- Each tool encapsulates one AI capability and is the only place that
  capability's logic lives (Single Responsibility).
- Tools receive a db Session via the agent constructor (Dependency Injection).
- Tools that do not need DB (LogTool, EditTool, ComplianceTool) are
  stateless and do not hold a db reference.
- The agent catches all tool errors and returns a safe fallback so the
  chat endpoint never raises an unhandled 500.
"""

import logging

from sqlalchemy.orm import Session

from app.ai.tools.compliance_tool import ComplianceTool
from app.ai.tools.edit_tool import EditTool
from app.ai.tools.followup_tool import FollowupTool
from app.ai.tools.log_tool import LogTool
from app.ai.tools.pdf_tool import PDFTool
from app.ai.tools.summary_tool import SummaryTool

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Intent constants
# ---------------------------------------------------------------------------

_INTENT_LOG = "log"
_INTENT_EDIT = "edit"
_INTENT_SUMMARY = "summary"
_INTENT_FOLLOWUP = "followup"
_INTENT_COMPLIANCE = "compliance"
_INTENT_PDF = "pdf"

# Keyword sets used for fast heuristic routing.
_EDIT_KEYWORDS = {"edit", "update", "change", "correct", "modify", "fix", "adjust"}
_SUMMARY_KEYWORDS = {"summary", "summarize", "summarise", "overview", "recap", "review"}
_FOLLOWUP_KEYWORDS = {"followup", "follow-up", "follow up", "next visit", "recommend", "recommendation"}
_COMPLIANCE_KEYWORDS = {"complian", "prohibited", "claim", "warning", "regulation", "policy"}
_PDF_KEYWORDS = {"pdf", "export", "report", "download", "print"}


class HCPCRMAgent:
    """
    Orchestrates all AI capabilities for the HCP CRM system.

    Parameters
    ----------
    db : Session
        SQLAlchemy session injected by FastAPI's dependency system.

    Example
    -------
    agent = HCPCRMAgent(db=db)
    result = agent.run(
        message="Summarize my recent visits",
        user_id=current_user.id,
    )
    """

    def __init__(self, db: Session) -> None:
        self.db = db
        # Stateless tools (no DB needed)
        self._log = LogTool()
        self._edit = EditTool()
        self._compliance = ComplianceTool()
        # Stateful tools (need DB session to call repositories)
        self._summary = SummaryTool(db)
        self._followup = FollowupTool(db)
        self._pdf = PDFTool(db)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(
        self,
        message: str,
        user_id: int,
        existing_draft: dict | None = None,
        interaction_id: int | None = None,
    ) -> dict:
        """
        Detect intent and delegate to the appropriate AI tool.

        Parameters
        ----------
        message : str
            The representative's natural language input.
        user_id : int
            Authenticated representative ID (used by tools that query DB).
        existing_draft : dict | None
            Current interaction draft from the chat session (passed to
            LogTool and EditTool for context-aware merging).
        interaction_id : int | None
            Specific interaction for summary / compliance / pdf / followup.

        Returns
        -------
        dict
            Keys always present: reply, merged_draft, missing_fields,
            warnings, intent. Optional key: pdf_content.
        """
        draft = existing_draft or {}
        intent = self._detect_intent(message)
        logger.info(
            "HCPCRMAgent user_id=%d intent=%s interaction_id=%s",
            user_id, intent, interaction_id,
        )

        try:
            return self._dispatch(intent, message, draft, user_id, interaction_id)
        except Exception as exc:
            logger.exception("HCPCRMAgent.run error intent=%s: %s", intent, exc)
            return {
                "reply": (
                    "I encountered an error while processing your request. "
                    "Please try again or contact support if the problem persists."
                ),
                "merged_draft": draft,
                "missing_fields": [],
                "warnings": [str(exc)],
                "intent": intent,
            }

    # ------------------------------------------------------------------
    # Intent detection
    # ------------------------------------------------------------------

    def _detect_intent(self, message: str) -> str:
        """
        Classify the user's intent using keyword heuristics.

        Keyword matching is evaluated in priority order so that more
        specific intents (edit, pdf) take precedence over the default log.

        Returns one of: log | edit | summary | followup | compliance | pdf
        """
        lowered = message.lower()

        if any(kw in lowered for kw in _EDIT_KEYWORDS):
            return _INTENT_EDIT
        if any(kw in lowered for kw in _PDF_KEYWORDS):
            return _INTENT_PDF
        if any(kw in lowered for kw in _COMPLIANCE_KEYWORDS):
            return _INTENT_COMPLIANCE
        if any(kw in lowered for kw in _FOLLOWUP_KEYWORDS):
            return _INTENT_FOLLOWUP
        if any(kw in lowered for kw in _SUMMARY_KEYWORDS):
            return _INTENT_SUMMARY

        return _INTENT_LOG

    # ------------------------------------------------------------------
    # Tool dispatch
    # ------------------------------------------------------------------

    def _dispatch(
        self,
        intent: str,
        message: str,
        draft: dict,
        user_id: int,
        interaction_id: int | None,
    ) -> dict:
        if intent == _INTENT_EDIT:
            return self._edit.run(message, draft)
        if intent == _INTENT_PDF:
            return self._pdf.run(user_id, interaction_id)
        if intent == _INTENT_COMPLIANCE:
            return self._compliance.run(message, draft)
        if intent == _INTENT_FOLLOWUP:
            return self._followup.run(user_id, interaction_id)
        if intent == _INTENT_SUMMARY:
            return self._summary.run(user_id, interaction_id)
        # Default: log
        return self._log.run(message, draft)
