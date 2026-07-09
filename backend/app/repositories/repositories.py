from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.domain.models import ChatMessage, ChatSession, Doctor, Interaction, User


class UserRepository:
    def __init__(self, db: Session): self.db = db
    def by_email(self, email: str): return self.db.scalar(select(User).where(User.email == email))
    def by_id(self, user_id: int): return self.db.get(User, user_id)
    def add(self, user: User): self.db.add(user); self.db.flush(); return user


class DoctorRepository:
    def __init__(self, db: Session): self.db = db
    def list(self, search: str | None = None):
        query = select(Doctor).order_by(Doctor.name)
        if search:
            query = query.where(func.lower(Doctor.name).contains(search.lower()))
        return list(self.db.scalars(query))
    def get(self, doctor_id: int): return self.db.get(Doctor, doctor_id)
    def by_name(self, name: str):
        return self.db.scalar(select(Doctor).where(func.lower(Doctor.name) == name.lower()))
    def add(self, doctor: Doctor): self.db.add(doctor); self.db.flush(); return doctor


class InteractionRepository:
    def __init__(self, db: Session): self.db = db
    def list_for_user(self, user_id: int):
        query = (
            select(Interaction).options(joinedload(Interaction.doctor))
            .where(Interaction.representative_id == user_id)
            .order_by(Interaction.date.desc(), Interaction.id.desc())
        )
        return list(self.db.scalars(query))
    def add(self, interaction: Interaction):
        self.db.add(interaction); self.db.flush(); self.db.refresh(interaction); return interaction


class ChatRepository:
    def __init__(self, db: Session): self.db = db
    def create(self, user_id: int):
        session = ChatSession(representative_id=user_id, current_draft={})
        self.db.add(session); self.db.flush(); return session
    def owned(self, session_id: int, user_id: int):
        return self.db.scalar(
            select(ChatSession).where(
                ChatSession.id == session_id, ChatSession.representative_id == user_id
            )
        )
    def message(self, session_id: int, role: str, content: str, payload: dict | None = None):
        row = ChatMessage(
            session_id=session_id, role=role, content=content, structured_payload=payload
        )
        self.db.add(row); self.db.flush(); return row
