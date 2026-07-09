from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.domain.models import ChatMessage, ChatSession, Doctor, Interaction, User  # noqa: E402,F401
