from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.domain.models import Doctor, Interaction, User
from app.repositories.repositories import (
    ChatRepository, DoctorRepository, InteractionRepository, UserRepository,
)
from app.schemas import DoctorCreate, InteractionCreate, LoginRequest, UserCreate


class AuthService:
    def __init__(self, db: Session): self.db, self.users = db, UserRepository(db)
    def register(self, data: UserCreate):
        if self.users.by_email(data.email):
            raise HTTPException(status.HTTP_409_CONFLICT, "Email is already registered")
        user = self.users.add(User(
            email=data.email.lower(), full_name=data.full_name,
            hashed_password=hash_password(data.password),
        ))
        self.db.commit()
        return user
    def login(self, data: LoginRequest):
        user = self.users.by_email(data.email.lower())
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password")
        if not user.is_active:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is inactive")
        return {"access_token": create_access_token(str(user.id)), "user": user}


class DoctorService:
    def __init__(self, db: Session): self.db, self.repo = db, DoctorRepository(db)
    def create(self, data: DoctorCreate):
        existing = self.repo.by_name(data.name)
        if existing: return existing
        doctor = self.repo.add(Doctor(**data.model_dump()))
        self.db.commit()
        return doctor


class InteractionService:
    def __init__(self, db: Session):
        self.db, self.interactions, self.doctors = (
            db, InteractionRepository(db), DoctorRepository(db)
        )
    def create(self, data: InteractionCreate, user_id: int):
        doctor = self.doctors.get(data.doctor_id) if data.doctor_id else None
        if not doctor and data.doctor_name:
            doctor = self.doctors.by_name(data.doctor_name)
        if not doctor and data.doctor_name:
            doctor = self.doctors.add(Doctor(name=data.doctor_name))
        if not doctor:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Select or name a doctor")
        values = data.model_dump(exclude={"doctor_name"}, exclude_none=True)
        values["doctor_id"] = doctor.id
        interaction = self.interactions.add(Interaction(**values, representative_id=user_id))
        self.db.commit()
        return interaction
