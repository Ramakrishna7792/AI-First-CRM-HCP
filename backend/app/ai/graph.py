import json
import re
from datetime import date

from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph

from app.ai.prompts import SYSTEM_PROMPT
from app.ai.state import InteractionGraphState
from app.core.config import settings
from app.schemas.interaction import InteractionDraft

ALLOWED = set(InteractionDraft.model_fields)


def _fallback_extract(message: str) -> dict:
    """Deterministic local extraction keeps the form useful without an API key."""
    result: dict = {"summary": message}
    lowered = message.lower()
    doctor = re.search(r"\bdr\.?\s+([A-Z][\w.-]+(?:\s+[A-Z][\w.-]+)*)", message)
    if doctor: result["doctor_name"] = f"Dr. {doctor.group(1)}"
    if "virtual" in lowered or "video" in lowered: result["interaction_type"] = "Virtual"
    elif "phone" in lowered or "call" in lowered: result["interaction_type"] = "Phone"
    else: result["interaction_type"] = "In-Person"
    for label in ("positive", "neutral", "negative"):
        if label in lowered: result["sentiment"] = label.title()
    if "today" in lowered: result["date"] = date.today().isoformat()
    return result


def extract_node(state: InteractionGraphState) -> dict:
    if not settings.groq_api_key:
        return {"extracted": _fallback_extract(state["message"]), "warnings": [
            "GROQ_API_KEY is not configured; basic local extraction was used."
        ]}
    llm = ChatGroq(
        api_key=settings.groq_api_key, model=settings.groq_model,
        temperature=0, model_kwargs={"response_format": {"type": "json_object"}},
    )
    response = llm.invoke(SYSTEM_PROMPT.format(message=state["message"]))
    raw = json.loads(response.content)
    return {"extracted": {key: value for key, value in raw.items() if key in ALLOWED}}


def validate_node(state: InteractionGraphState) -> dict:
    merged = {**state.get("existing_draft", {}), **state.get("extracted", {})}
    valid = InteractionDraft.model_validate(merged).model_dump(mode="json", exclude_none=True)
    missing = [field for field in ("doctor_name", "date", "summary") if not valid.get(field)]
    reply = (
        "I populated the interaction draft. Please review it before saving."
        if not missing else f"I captured the details so far. Please provide: {', '.join(missing)}."
    )
    return {"merged_draft": valid, "missing_fields": missing, "reply": reply}


builder = StateGraph(InteractionGraphState)
builder.add_node("extract", extract_node)
builder.add_node("validate", validate_node)
builder.add_edge(START, "extract")
builder.add_edge("extract", "validate")
builder.add_edge("validate", END)
interaction_graph = builder.compile()


def run_interaction_graph(message: str, existing_draft: dict | None = None) -> dict:
    return interaction_graph.invoke({
        "message": message, "existing_draft": existing_draft or {}, "extracted": {},
        "merged_draft": {}, "reply": "", "missing_fields": [], "warnings": [],
    })
