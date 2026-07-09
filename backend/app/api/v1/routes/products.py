from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domain.models import User
from app.repositories.repositories import ProductRepository
from app.schemas import ProductCreate, ProductRead, ProductUpdate
from app.services.services import ProductService

router = APIRouter()


@router.get("", response_model=list[ProductRead])
def list_products(
    search: str | None = Query(None, max_length=100), active_only: bool = False,
    offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db), _: User = Depends(get_current_user),
):
    return ProductRepository(db).list(search, active_only, offset, limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user),
):
    return ProductService(db).get(product_id)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user),
):
    return ProductService(db).create(data)


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int, data: ProductUpdate, db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return ProductService(db).update(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user),
):
    ProductService(db).delete(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
