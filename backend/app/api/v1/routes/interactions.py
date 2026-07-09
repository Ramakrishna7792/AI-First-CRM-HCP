from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domain.models import User
from app.repositories.repositories import InteractionRepository
from app.schemas import InteractionCreate, InteractionRead
from app.services.services import InteractionService

router = APIRouter()


@router.get("", response_model=list[InteractionRead])
def list_interactions(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return InteractionRepository(db).list_for_user(user.id)


@router.post("", response_model=InteractionRead, status_code=201)
def create_interaction(
    data: InteractionCreate, db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return InteractionService(db).create(data, user.id)
