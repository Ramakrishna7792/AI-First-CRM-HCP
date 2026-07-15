from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.agent import HCPCRMAgent
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

    # Route through HCPCRMAgent — detects intent and delegates to the
    # appropriate AI tool. Falls back gracefully if Groq is unavailable.
    agent = HCPCRMAgent(db=db)
    result = agent.run(
        message=data.message,
        user_id=user.id,
        existing_draft=session.current_draft,
    )

    session.current_draft = result.get("merged_draft", session.current_draft)
    repo.message(session.id, "assistant", result["reply"], result.get("merged_draft"))
    db.commit()

    return ChatResponse(
        session_id=session.id,
        reply=result["reply"],
        interaction_draft=InteractionDraft.model_validate(result.get("merged_draft", {})),
        missing_fields=result.get("missing_fields", []),
        validation_warnings=result.get("warnings", []),
    )
