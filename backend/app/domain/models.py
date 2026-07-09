from datetime import date, datetime, time

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, JSON, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(40), default="representative")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Doctor(Base, TimestampMixin):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    specialization: Mapped[str | None] = mapped_column(String(255))
    hospital: Mapped[str | None] = mapped_column(String(255))
    city: Mapped[str | None] = mapped_column(String(100), index=True)
    interactions: Mapped[list["Interaction"]] = relationship(back_populates="doctor")


class Interaction(Base, TimestampMixin):
    __tablename__ = "interactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), index=True)
    representative_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    interaction_type: Mapped[str] = mapped_column(String(100), default="In-Person")
    date: Mapped[date] = mapped_column(Date)
    time: Mapped[time | None] = mapped_column(Time)
    attendees: Mapped[str | None] = mapped_column(Text)
    topics: Mapped[str | None] = mapped_column(Text)
    materials: Mapped[str | None] = mapped_column(Text)
    samples: Mapped[str | None] = mapped_column(Text)
    sentiment: Mapped[str | None] = mapped_column(String(50))
    outcomes: Mapped[str | None] = mapped_column(Text)
    followup: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text)
    entry_source: Mapped[str] = mapped_column(String(30), default="form")
    doctor: Mapped[Doctor] = relationship(back_populates="interactions")


class ChatSession(Base, TimestampMixin):
    __tablename__ = "chat_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    representative_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(30), default="active")
    current_draft: Mapped[dict] = mapped_column(JSON, default=dict)
    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("chat_sessions.id"), index=True)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    structured_payload: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    session: Mapped[ChatSession] = relationship(back_populates="messages")
