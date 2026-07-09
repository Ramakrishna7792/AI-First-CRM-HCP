from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DoctorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    specialization: str | None = None
    hospital: str | None = None
    city: str | None = None


class DoctorRead(DoctorCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
