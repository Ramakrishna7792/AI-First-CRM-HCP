from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domain.models import User
from app.schemas import LoginRequest, Token, UserCreate, UserRead
from app.services.services import AuthService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register(data)


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(db).login(data)


@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)):
    return user
