from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domain.models import User
from app.repositories.repositories import InteractionRepository
from app.schemas import InteractionCreate, InteractionRead, InteractionUpdate
from app.services.services import InteractionService

router = APIRouter()


@router.get("", response_model=list[InteractionRead])
def list_interactions(
    doctor_id: int | None = None, offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return InteractionRepository(db).list_for_user(user.id, doctor_id, offset, limit)


@router.get("/{interaction_id}", response_model=InteractionRead)
def get_interaction(
    interaction_id: int, db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return InteractionService(db).get(interaction_id, user.id)


@router.post("", response_model=InteractionRead, status_code=status.HTTP_201_CREATED)
def create_interaction(
    data: InteractionCreate, db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return InteractionService(db).create(data, user.id)


@router.patch("/{interaction_id}", response_model=InteractionRead)
def update_interaction(
    interaction_id: int, data: InteractionUpdate, db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return InteractionService(db).update(interaction_id, data, user.id)


@router.delete("/{interaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interaction(
    interaction_id: int, db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    InteractionService(db).delete(interaction_id, user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
