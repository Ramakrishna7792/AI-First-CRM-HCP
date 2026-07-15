"""
Edit Tool

Handles AI-assisted interaction edits.

The user's edit instruction is merged with the existing draft using the
same LangGraph extraction pipeline. LangGraph's validate_node merges
newly extracted fields on top of the existing draft, so no duplicate
merge logic is needed here.
"""

import logging

logger = logging.getLogger(__name__)


class EditTool:
    """
    Understand an edit request and return an updated interaction draft.

    Reuses the LangGraph extraction pipeline which deep-merges newly
    extracted values over the existing draft, giving natural edit behaviour.
    """

    def run(self, message: str, existing_draft: dict) -> dict:
        """
        Merge edit instructions into the current draft.

        Parameters
        ----------
        message : str
            The representative's edit instruction (e.g. "change the date to tomorrow").
        existing_draft : dict
            The current interaction draft stored in the chat session.

        Returns
        -------
        dict
            Keys: merged_draft, missing_fields, reply, warnings, intent.
        """
        logger.debug(
            "EditTool.run existing_draft_keys=%s",
            list(existing_draft.keys()),
        )
        from app.ai.graph import run_interaction_graph  # lazy: avoids langgraph at module load
        result = run_interaction_graph(message, existing_draft)
        result["intent"] = "edit"

        # Humanise the reply to reflect that an update occurred.
        if result.get("reply"):
            result["reply"] = result["reply"].replace(
                "I populated the interaction draft",
                "I updated the interaction draft",
            )
        return result
