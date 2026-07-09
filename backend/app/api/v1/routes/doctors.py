from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domain.models import User
from app.repositories.repositories import DoctorRepository
from app.schemas import DoctorCreate, DoctorRead, DoctorUpdate
from app.services.services import DoctorService

router = APIRouter()


@router.get("", response_model=list[DoctorRead])
def list_doctors(
    search: str | None = Query(None, max_length=100),
    offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db), _: User = Depends(get_current_user),
):
    return DoctorRepository(db).list(search, offset, limit)


@router.get("/{doctor_id}", response_model=DoctorRead)
def get_doctor(
    doctor_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user),
):
    return DoctorService(db).get(doctor_id)


@router.post("", response_model=DoctorRead, status_code=status.HTTP_201_CREATED)
def create_doctor(
    data: DoctorCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user),
):
    return DoctorService(db).create(data)


@router.patch("/{doctor_id}", response_model=DoctorRead)
def update_doctor(
    doctor_id: int, data: DoctorUpdate, db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return DoctorService(db).update(doctor_id, data)


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(
    doctor_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user),
):
    DoctorService(db).delete(doctor_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
