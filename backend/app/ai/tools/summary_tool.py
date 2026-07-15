"""
Summary Tool

Fetches the representative's recent interaction history and summarizes it
using Groq. Falls back to a deterministic local summary when the API key
is absent so the tool is always usable in development.

Uses the existing InteractionRepository — no raw SQLAlchemy queries here.
"""

import logging

from sqlalchemy.orm import Session

from app.repositories.repositories import InteractionRepository

logger = logging.getLogger(__name__)

_SUMMARY_SYSTEM_PROMPT = """You are a Healthcare CRM assistant for a Medical Representative.

Summarize the following doctor interaction history concisely and actionably.

Focus on:
- Doctors visited and their specializations
- Products discussed and doctor reception
- Key concerns or objections raised
- Outcomes and commitments made
- Follow-up actions and timelines
- Overall relationship trend (improving / stable / at-risk)

Keep the summary under 200 words. Use bullet points where helpful."""


class SummaryTool:
    """
    Summarize a representative's recent interaction history.

    Reads from the existing InteractionRepository and calls Groq for
    natural language summarization.
    """

    def __init__(self, db: Session) -> None:
        self.repo = InteractionRepository(db)

    def run(self, user_id: int, interaction_id: int | None = None) -> dict:
        """
        Fetch interactions and return an AI-generated summary.

        Parameters
        ----------
        user_id : int
            The authenticated representative's ID.
        interaction_id : int | None
            If provided, summarizes only that specific interaction.

        Returns
        -------
        dict
            Keys: reply, merged_draft, missing_fields, warnings, intent.
        """
        if interaction_id:
            interaction = self.repo.get_for_user(interaction_id, user_id)
            interactions = [interaction] if interaction else []
        else:
            interactions = self.repo.list_for_user(user_id, limit=10)

        if not interactions:
            return self._empty_result("No interaction history found to summarize.")

        interaction_text = self._format_interactions(interactions)

        try:
            summary = self._call_llm(interaction_text)
        except Exception as exc:
            logger.warning("SummaryTool LLM call failed: %s", exc)
            summary = self._local_summary(interactions)

        return {
            "reply": summary,
            "merged_draft": {},
            "missing_fields": [],
            "warnings": [],
            "intent": "summary",
        }

    @staticmethod
    def _format_interactions(interactions) -> str:
        lines = []
        for ix in interactions:
            products = ", ".join(p.product_name for p in ix.products) or "None"
            lines.append(
                f"• {ix.date} | Dr. {ix.doctor.name}"
                f" ({ix.doctor.specialization or 'General'})"
                f" | Type: {ix.interaction_type}"
                f" | Sentiment: {ix.sentiment or 'N/A'}"
                f" | Products: {products}"
                f" | Summary: {ix.summary}"
            )
        return "\n".join(lines)

    @staticmethod
    def _local_summary(interactions) -> str:
        """Deterministic fallback — no LLM required."""
        count = len(interactions)
        doctors = sorted({ix.doctor.name for ix in interactions})
        sentiments = [ix.sentiment for ix in interactions if ix.sentiment]
        positive = sentiments.count("Positive")
        return (
            f"You have {count} recorded interaction(s) with "
            f"{', '.join(doctors)}. "
            f"{positive} of {len(sentiments)} rated interactions had positive sentiment."
        )

    def _call_llm(self, text: str) -> str:
        from app.core.config import settings
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY not configured")
        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0.2,
        )
        messages = [
            SystemMessage(content=_SUMMARY_SYSTEM_PROMPT),
            HumanMessage(content=text),
        ]
        return llm.invoke(messages).content.strip()

    @staticmethod
    def _empty_result(reply: str) -> dict:
        return {
            "reply": reply,
            "merged_draft": {},
            "missing_fields": [],
            "warnings": [],
            "intent": "summary",
        }
