from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.domain.models import ChatMessage, ChatSession, Doctor, Interaction, Product, User


class BaseRepository:
    model = None

    def __init__(self, db: Session):
        self.db = db

    def get(self, entity_id: int):
        return self.db.get(self.model, entity_id)

    def add(self, entity):
        self.db.add(entity)
        self.db.flush()
        return entity

    def delete(self, entity) -> None:
        self.db.delete(entity)
        self.db.flush()

    @staticmethod
    def apply_changes(entity, values: dict):
        for field, value in values.items():
            setattr(entity, field, value)
        return entity


class UserRepository(BaseRepository):
    model = User

    def by_email(self, email: str):
        return self.db.scalar(select(User).where(User.email == email))

    def by_id(self, user_id: int):
        return self.get(user_id)


class DoctorRepository(BaseRepository):
    model = Doctor

    def list(self, search: str | None = None, offset: int = 0, limit: int = 100):
        query = select(Doctor).order_by(Doctor.name).offset(offset).limit(limit)
        if search:
            term = f"%{search.lower()}%"
            query = query.where(
                func.lower(Doctor.name).like(term)
                | func.lower(func.coalesce(Doctor.specialization, "")).like(term)
                | func.lower(func.coalesce(Doctor.city, "")).like(term)
            )
        return list(self.db.scalars(query))

    def by_name(self, name: str):
        return self.db.scalar(select(Doctor).where(func.lower(Doctor.name) == name.lower()))


class ProductRepository(BaseRepository):
    model = Product

    def list(
        self, search: str | None = None, active_only: bool = False,
        offset: int = 0, limit: int = 100,
    ):
        query = select(Product).order_by(Product.product_name).offset(offset).limit(limit)
        if search:
            term = f"%{search.lower()}%"
            query = query.where(
                func.lower(Product.product_name).like(term)
                | func.lower(func.coalesce(Product.category, "")).like(term)
            )
        if active_only:
            query = query.where(Product.is_active.is_(True))
        return list(self.db.scalars(query))

    def by_name(self, name: str):
        return self.db.scalar(
            select(Product).where(func.lower(Product.product_name) == name.lower())
        )

    def by_ids(self, product_ids: Sequence[int]):
        if not product_ids:
            return []
        return list(self.db.scalars(select(Product).where(Product.id.in_(product_ids))))


class InteractionRepository(BaseRepository):
    model = Interaction

    def _detail_query(self):
        return select(Interaction).options(
            joinedload(Interaction.doctor), selectinload(Interaction.products)
        )

    def get_for_user(self, interaction_id: int, user_id: int):
        return self.db.scalar(
            self._detail_query().where(
                Interaction.id == interaction_id,
                Interaction.representative_id == user_id,
            )
        )

    def list_for_user(
        self, user_id: int, doctor_id: int | None = None,
        offset: int = 0, limit: int = 100,
    ):
        query = (
            self._detail_query()
            .where(Interaction.representative_id == user_id)
            .order_by(Interaction.date.desc(), Interaction.id.desc())
            .offset(offset).limit(limit)
        )
        if doctor_id is not None:
            query = query.where(Interaction.doctor_id == doctor_id)
        return list(self.db.scalars(query))

    def add(self, interaction: Interaction):
        super().add(interaction)
        self.db.refresh(interaction)
        return self.get_for_user(interaction.id, interaction.representative_id)


class ChatRepository(BaseRepository):
    model = ChatSession

    def create(self, user_id: int):
        return self.add(ChatSession(representative_id=user_id, current_draft={}))

    def owned(self, session_id: int, user_id: int):
        return self.db.scalar(select(ChatSession).where(
            ChatSession.id == session_id, ChatSession.representative_id == user_id
        ))

    def message(self, session_id: int, role: str, content: str, payload: dict | None = None):
        row = ChatMessage(
            session_id=session_id, role=role, content=content, structured_payload=payload
        )
        self.db.add(row)
        self.db.flush()
        return row
