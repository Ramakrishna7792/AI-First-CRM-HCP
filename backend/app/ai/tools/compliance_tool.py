"""
Compliance Checker Tool

Detects prohibited medical claims, misleading efficacy statements, missing
mandatory safety information, and other compliance risks in interaction notes.

Returns structured warnings suitable for display in the frontend.
Falls back to an "UNKNOWN" status (non-blocking) when the API key is absent.
"""

import json
import logging

logger = logging.getLogger(__name__)

_COMPLIANCE_SYSTEM_PROMPT = """You are a pharmaceutical compliance officer reviewing a Medical Representative's interaction note.

Check the text for the following compliance issues:
- Off-label promotion or prohibited medical claims
- Misleading efficacy or safety statements
- Unsupported or exaggerated clinical claims
- Missing mandatory product safety information
- Promises outside approved product labelling

Return ONLY valid JSON in this exact format (no markdown, no extra text):
{
    "status": "PASS",
    "warnings": []
}

Rules:
- status must be exactly "PASS" or "FAIL"
- warnings is a list of strings; empty list if status is PASS
- Be specific in each warning — quote the problematic text where possible"""


class ComplianceTool:
    """
    Check interaction content for pharmaceutical compliance issues.

    Stateless — no database access needed. Operates on the current
    draft summary or the raw user message.
    """

    def run(self, message: str, existing_draft: dict) -> dict:
        """
        Analyse the interaction note for compliance issues.

        Prefers the draft summary field when available since it contains
        the most structured version of the interaction.

        Parameters
        ----------
        message : str
            The user's raw chat message (used when no draft summary exists).
        existing_draft : dict
            The current interaction draft; summary field used if present.

        Returns
        -------
        dict
            Keys: reply, merged_draft, missing_fields, warnings, intent.
        """
        text = (existing_draft.get("summary") or "").strip() or message.strip()

        try:
            result = self._call_llm(text)
            warnings = result.get("warnings", [])
            status = result.get("status", "UNKNOWN")
        except Exception as exc:
            logger.warning("ComplianceTool LLM failed: %s", exc)
            warnings = []
            status = "UNKNOWN"

        reply = self._build_reply(status, warnings)

        return {
            "reply": reply,
            "merged_draft": existing_draft,
            "missing_fields": [],
            "warnings": warnings,
            "intent": "compliance",
        }

    def _call_llm(self, text: str) -> dict:
        from app.core.config import settings
        if not settings.groq_api_key:
            return {
                "status": "UNKNOWN",
                "warnings": [
                    "GROQ_API_KEY is not configured. "
                    "Compliance check skipped — configure the API key for production use."
                ],
            }
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0.1,
            model_kwargs={"response_format": {"type": "json_object"}},
        )
        from langchain_core.messages import HumanMessage, SystemMessage
        messages = [
            SystemMessage(content=_COMPLIANCE_SYSTEM_PROMPT),
            HumanMessage(content=text),
        ]
        raw = llm.invoke(messages).content
        return json.loads(raw)

    @staticmethod
    def _build_reply(status: str, warnings: list[str]) -> str:
        if status == "PASS":
            return "✅ Compliance check passed. No issues detected in this interaction note."
        if status == "UNKNOWN":
            if warnings:
                return f"ℹ️ Compliance check could not run:\n\n" + "\n".join(f"• {w}" for w in warnings)
            return "ℹ️ Compliance check skipped (API key not configured)."
        # FAIL
        items = "\n".join(f"• {w}" for w in warnings) if warnings else "Review required."
        return f"⚠️ Compliance check FAILED. Please review:\n\n{items}"
