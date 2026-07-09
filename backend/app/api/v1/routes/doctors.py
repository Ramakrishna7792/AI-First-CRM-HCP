from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domain.models import User
from app.repositories.repositories import DoctorRepository
from app.schemas import DoctorCreate, DoctorRead
from app.services.services import DoctorService

router = APIRouter()


@router.get("", response_model=list[DoctorRead])
def list_doctors(
    search: str | None = Query(None, max_length=100),
    db: Session = Depends(get_db), _: User = Depends(get_current_user),
):
    return DoctorRepository(db).list(search)


@router.post("", response_model=DoctorRead, status_code=201)
def create_doctor(
    data: DoctorCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user),
):
    return DoctorService(db).create(data)
