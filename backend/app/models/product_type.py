from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4

class ProductTypeBase(BaseModel):
    name: str

class ProductTypeCreate(ProductTypeBase):
    pass

class ProductTypeUpdate(ProductTypeBase):
    pass

class ProductTypeInDB(ProductTypeBase):
    type_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProductTypeRead(ProductTypeBase):
    type_id: str
    created_at: datetime
    product_count: int = 0  # Number of products using this type

    class Config:
        from_attributes = True
