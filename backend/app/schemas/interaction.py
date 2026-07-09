from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.doctor import DoctorRead


class InteractionDraft(BaseModel):
    doctor_id: int | None = None
    doctor_name: str | None = None
    interaction_type: str | None = None
    date: date | None = None
    time: time | None = None
    attendees: str | None = None
    topics: str | None = None
    materials: str | None = None
    samples: str | None = None
    sentiment: str | None = Field(None, pattern="^(Positive|Neutral|Negative)$")
    outcomes: str | None = None
    followup: str | None = None
    summary: str | None = None


class InteractionCreate(InteractionDraft):
    doctor_id: int | None = None
    doctor_name: str | None = None
    date: date
    summary: str = Field(min_length=3)
    entry_source: str = Field(default="form", pattern="^(form|ai_assisted)$")


class InteractionRead(InteractionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    doctor_id: int
    representative_id: int
    doctor: DoctorRead
    created_at: datetime
