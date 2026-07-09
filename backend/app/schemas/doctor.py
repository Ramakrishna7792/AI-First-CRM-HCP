from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DoctorBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    specialization: str | None = Field(None, max_length=255)
    hospital: str | None = Field(None, max_length=255)
    city: str | None = Field(None, max_length=100)


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=255)
    specialization: str | None = Field(None, max_length=255)
    hospital: str | None = Field(None, max_length=255)
    city: str | None = Field(None, max_length=100)


class DoctorRead(DoctorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
