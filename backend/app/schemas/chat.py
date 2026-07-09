from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.interaction import InteractionDraft


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)


class ChatResponse(BaseModel):
    session_id: int
    reply: str
    interaction_draft: InteractionDraft
    missing_fields: list[str]
    validation_warnings: list[str] = []
    requires_confirmation: bool = True


class ChatSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    current_draft: dict
    created_at: datetime
