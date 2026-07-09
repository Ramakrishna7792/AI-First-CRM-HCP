from __future__ import annotations

from datetime import date as DateType
from datetime import datetime
from datetime import time as TimeType

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.doctor import DoctorRead
from app.schemas.product import ProductRead


class InteractionDraft(BaseModel):
    doctor_id: int | None = None
    doctor_name: str | None = None
    interaction_type: str | None = None
    date: DateType | None = None
    time: TimeType | None = None
    attendees: str | None = None
    topics: str | None = None
    materials: str | None = None
    samples: str | None = None
    sentiment: str | None = Field(None, pattern="^(Positive|Neutral|Negative)$")
    outcomes: str | None = None
    followup: str | None = None
    summary: str | None = None


class InteractionCreate(InteractionDraft):
    date: DateType
    summary: str = Field(min_length=3)
    entry_source: str = Field(default="form", pattern="^(form|ai_assisted)$")
    product_ids: list[int] = Field(default_factory=list)


class InteractionUpdate(BaseModel):
    doctor_id: int | None = None
    interaction_type: str | None = None
    date: DateType | None = None
    time: TimeType | None = None
    attendees: str | None = None
    topics: str | None = None
    materials: str | None = None
    samples: str | None = None
    sentiment: str | None = Field(None, pattern="^(Positive|Neutral|Negative)$")
    outcomes: str | None = None
    followup: str | None = None
    summary: str | None = Field(None, min_length=3)
    product_ids: list[int] | None = None


class InteractionRead(InteractionDraft):
    model_config = ConfigDict(from_attributes=True)
    id: int
    doctor_id: int
    representative_id: int
    entry_source: str
    doctor: DoctorRead
    products: list[ProductRead]
    created_at: datetime
    updated_at: datetime
