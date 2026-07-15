"""
Follow-up Recommendation Tool

Analyzes a representative's recent doctor visit history and generates a
prioritized, actionable follow-up recommendation using Groq.

Falls back to a rule-based local recommendation when the API key is absent.
Uses the existing InteractionRepository — no raw SQLAlchemy queries here.
"""

import logging

from sqlalchemy.orm import Session

from app.repositories.repositories import InteractionRepository

logger = logging.getLogger(__name__)

_FOLLOWUP_SYSTEM_PROMPT = """You are an experienced Medical Representative coach at a pharmaceutical company.

Analyze the following doctor interaction history and recommend the optimal follow-up strategy.

Your recommendation must include:
1. Follow-up Priority — High / Medium / Low (with brief justification)
2. Recommended Visit Interval — e.g. "within 1 week", "in 2 weeks", "monthly"
3. Key Talking Points — 2–3 specific discussion items for the next visit
4. Samples to Bring — specific products and quantities if applicable
5. Materials to Prepare — brochures, clinical studies, or digital assets
6. Doctor Concerns to Address — any objections or questions raised in past visits

Be specific, practical, and concise. Base your recommendation only on the data provided."""


class FollowupTool:
    """
    Recommend prioritized follow-up actions based on interaction history.

    Reads from the existing InteractionRepository and calls Groq for
    intelligent, context-aware recommendations.
    """

    def __init__(self, db: Session) -> None:
        self.repo = InteractionRepository(db)

    def run(self, user_id: int, interaction_id: int | None = None) -> dict:
        """
        Analyze interaction history and return follow-up recommendations.

        Parameters
        ----------
        user_id : int
            The authenticated representative's ID.
        interaction_id : int | None
            If provided, focuses on the doctor from that specific interaction.

        Returns
        -------
        dict
            Keys: reply, merged_draft, missing_fields, warnings, intent.
        """
        doctor_id: int | None = None
        if interaction_id:
            interaction = self.repo.get_for_user(interaction_id, user_id)
            if interaction:
                doctor_id = interaction.doctor_id

        interactions = self.repo.list_for_user(user_id, doctor_id=doctor_id, limit=5)

        if not interactions:
            return self._empty_result(
                "No interaction history found. "
                "Log your first doctor visit to receive follow-up recommendations."
            )

        context = self._build_context(interactions)

        try:
            recommendation = self._call_llm(context)
        except Exception as exc:
            logger.warning("FollowupTool LLM call failed: %s", exc)
            recommendation = self._local_recommendation(interactions)

        return {
            "reply": recommendation,
            "merged_draft": {},
            "missing_fields": [],
            "warnings": [],
            "intent": "followup",
        }

    @staticmethod
    def _build_context(interactions) -> str:
        lines = []
        for ix in interactions:
            products = ", ".join(p.product_name for p in ix.products) or "None"
            lines.append(
                f"• Visit {ix.date} | Dr. {ix.doctor.name}"
                f" ({ix.doctor.specialization or 'General'},"
                f" {ix.doctor.hospital or 'unknown hospital'})"
                f" | Type: {ix.interaction_type}"
                f" | Sentiment: {ix.sentiment or 'N/A'}"
                f" | Products: {products}"
                f" | Outcome: {ix.outcomes or 'N/A'}"
                f" | Planned follow-up: {ix.followup or 'None noted'}"
            )
        return "\n".join(lines)

    @staticmethod
    def _local_recommendation(interactions) -> str:
        """Rule-based fallback — no LLM required."""
        latest = interactions[0]
        sentiment = latest.sentiment or "Neutral"
        priority_map = {"Positive": "High", "Neutral": "Medium", "Negative": "High"}
        priority = priority_map.get(sentiment, "Medium")
        interval = "within 1 week" if sentiment == "Positive" else "within 2 weeks"
        return (
            f"Follow-up Priority: {priority}\n\n"
            f"Last visit with Dr. {latest.doctor.name} was on {latest.date} "
            f"with {sentiment.lower()} sentiment.\n\n"
            f"Recommended visit interval: {interval}.\n"
            f"Review previous topics and follow-up notes before your next visit."
        )

    def _call_llm(self, context: str) -> str:
        from app.core.config import settings
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY not configured")
        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0.3,
        )
        messages = [
            SystemMessage(content=_FOLLOWUP_SYSTEM_PROMPT),
            HumanMessage(content=context),
        ]
        return llm.invoke(messages).content.strip()

    @staticmethod
    def _empty_result(reply: str) -> dict:
        return {
            "reply": reply,
            "merged_draft": {},
            "missing_fields": [],
            "warnings": [],
            "intent": "followup",
        }
