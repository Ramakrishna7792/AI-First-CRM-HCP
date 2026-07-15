"""
Log Tool

Wraps the LangGraph extraction pipeline to log new interactions.

This tool does NOT persist data directly.
The extracted draft is returned to the frontend for user review.
Saving is performed by InteractionService via the normal POST /interactions API.
"""

import logging

logger = logging.getLogger(__name__)


class LogTool:
    """
    Extract interaction fields from free-text and return a structured draft.

    Delegates entirely to the existing LangGraph extract→validate pipeline
    so no duplication of extraction logic occurs here.
    """

    def run(self, message: str, existing_draft: dict) -> dict:
        """
        Extract interaction data from the user's natural language message.

        Parameters
        ----------
        message : str
            The representative's free-text visit note.
        existing_draft : dict
            Any previously extracted fields from this chat session.

        Returns
        -------
        dict
            Keys: merged_draft, missing_fields, reply, warnings, intent.
        """
        logger.debug("LogTool.run message_length=%d", len(message))
        from app.ai.graph import run_interaction_graph  # lazy: avoids langgraph at module load
        result = run_interaction_graph(message, existing_draft)
        result["intent"] = "log"
        return result
