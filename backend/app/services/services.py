from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.domain.models import Doctor, Interaction, Product, User
from app.repositories.repositories import (
    DoctorRepository, InteractionRepository, ProductRepository, UserRepository,
)
from app.schemas import (
    DoctorCreate, DoctorUpdate, InteractionCreate, InteractionUpdate, LoginRequest,
    ProductCreate, ProductUpdate, UserCreate,
)


def not_found(entity: str) -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, f"{entity} not found")


class TransactionalService:
    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(status.HTTP_409_CONFLICT, "A conflicting record already exists") from exc


class AuthService(TransactionalService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.users = UserRepository(db)

    def register(self, data: UserCreate):
        if self.users.by_email(data.email):
            raise HTTPException(status.HTTP_409_CONFLICT, "Email is already registered")
        user = self.users.add(User(
            email=data.email.lower(), full_name=data.full_name,
            hashed_password=hash_password(data.password),
        ))
        self.commit()
        return user

    def login(self, data: LoginRequest):
        user = self.users.by_email(data.email.lower())
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password")
        if not user.is_active:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is inactive")
        return {"access_token": create_access_token(str(user.id)), "user": user}


class DoctorService(TransactionalService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.repo = DoctorRepository(db)

    def get(self, doctor_id: int):
        doctor = self.repo.get(doctor_id)
        if not doctor:
            raise not_found("Doctor")
        return doctor

    def create(self, data: DoctorCreate):
        if self.repo.by_name(data.name):
            raise HTTPException(status.HTTP_409_CONFLICT, "Doctor already exists")
        doctor = self.repo.add(Doctor(**data.model_dump()))
        self.commit()
        return doctor

    def update(self, doctor_id: int, data: DoctorUpdate):
        doctor = self.get(doctor_id)
        self.repo.apply_changes(doctor, data.model_dump(exclude_unset=True))
        self.commit()
        return doctor

    def delete(self, doctor_id: int):
        doctor = self.get(doctor_id)
        self.repo.delete(doctor)
        self.commit()


class ProductService(TransactionalService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.repo = ProductRepository(db)

    def get(self, product_id: int):
        product = self.repo.get(product_id)
        if not product:
            raise not_found("Product")
        return product

    def create(self, data: ProductCreate):
        if self.repo.by_name(data.product_name):
            raise HTTPException(status.HTTP_409_CONFLICT, "Product already exists")
        product = self.repo.add(Product(**data.model_dump()))
        self.commit()
        return product

    def update(self, product_id: int, data: ProductUpdate):
        product = self.get(product_id)
        self.repo.apply_changes(product, data.model_dump(exclude_unset=True))
        self.commit()
        return product

    def delete(self, product_id: int):
        product = self.get(product_id)
        self.repo.delete(product)
        self.commit()


class InteractionService(TransactionalService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.interactions = InteractionRepository(db)
        self.doctors = DoctorRepository(db)
        self.products = ProductRepository(db)

    def get(self, interaction_id: int, user_id: int):
        interaction = self.interactions.get_for_user(interaction_id, user_id)
        if not interaction:
            raise not_found("Interaction")
        return interaction

    def _products(self, product_ids: list[int]):
        products = self.products.by_ids(product_ids)
        if len(products) != len(set(product_ids)):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "One or more products do not exist")
        return products

    def create(self, data: InteractionCreate, user_id: int):
        doctor = self.doctors.get(data.doctor_id) if data.doctor_id else None
        if not doctor and data.doctor_name:
            doctor = self.doctors.by_name(data.doctor_name)
        if not doctor and data.doctor_name:
            doctor = self.doctors.add(Doctor(name=data.doctor_name))
        if not doctor:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Select or name a doctor")
        values = data.model_dump(exclude={"doctor_name", "product_ids"}, exclude_none=True)
        values["doctor_id"] = doctor.id
        interaction = Interaction(**values, representative_id=user_id)
        interaction.products = self._products(data.product_ids)
        interaction = self.interactions.add(interaction)
        self.commit()
        return interaction

    def update(self, interaction_id: int, data: InteractionUpdate, user_id: int):
        interaction = self.get(interaction_id, user_id)
        values = data.model_dump(exclude={"product_ids"}, exclude_unset=True)
        if "doctor_id" in values and not self.doctors.get(values["doctor_id"]):
            raise not_found("Doctor")
        self.interactions.apply_changes(interaction, values)
        if data.product_ids is not None:
            interaction.products = self._products(data.product_ids)
        self.commit()
        return self.interactions.get_for_user(interaction_id, user_id)

    def delete(self, interaction_id: int, user_id: int):
        interaction = self.get(interaction_id, user_id)
        self.interactions.delete(interaction)
        self.commit()
