from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.graph import run_interaction_graph
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domain.models import User
from app.repositories.repositories import ChatRepository
from app.schemas import ChatRequest, ChatResponse, ChatSessionRead, InteractionDraft

router = APIRouter()


@router.post("/sessions", response_model=ChatSessionRead, status_code=201)
def create_session(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    session = ChatRepository(db).create(user.id)
    db.commit()
    return session


@router.post("/sessions/{session_id}/messages", response_model=ChatResponse)
def send_message(
    session_id: int, data: ChatRequest, db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    repo = ChatRepository(db)
    session = repo.owned(session_id, user.id)
    if not session:
        raise HTTPException(404, "Chat session not found")
    repo.message(session.id, "user", data.message)
    result = run_interaction_graph(data.message, session.current_draft)
    session.current_draft = result["merged_draft"]
    repo.message(session.id, "assistant", result["reply"], result["merged_draft"])
    db.commit()
    return ChatResponse(
        session_id=session.id, reply=result["reply"],
        interaction_draft=InteractionDraft.model_validate(result["merged_draft"]),
        missing_fields=result["missing_fields"], validation_warnings=result.get("warnings", []),
    )
