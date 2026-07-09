from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    product_name: str = Field(min_length=2, max_length=255)
    category: str | None = Field(None, max_length=100)
    description: str | None = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: str | None = Field(None, min_length=2, max_length=255)
    category: str | None = Field(None, max_length=100)
    description: str | None = None
    is_active: bool | None = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
