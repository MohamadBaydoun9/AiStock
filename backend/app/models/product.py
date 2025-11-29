from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from uuid import uuid4

class ProductBase(BaseModel):
    product_name: str
    product_type: str
    price_predicted: float
    price_modified: Optional[float] = None
    quantity: int = 0
    published: bool = False  # Public visibility
    # Metadata fields
    age_months: Optional[int] = None
    weight_kg: Optional[float] = None
    health_status: Optional[int] = None  # 0=normal, 1=good, 2=excellent
    vaccinated: Optional[bool] = None
    country: Optional[str] = None
    predicted_breed: Optional[str] = None
    prediction_confidence: Optional[float] = None


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    product_type: Optional[str] = None
    price_modified: Optional[float] = None
    quantity: Optional[int] = None
    published: Optional[bool] = None
    # Metadata fields
    age_months: Optional[int] = None
    weight_kg: Optional[float] = None
    health_status: Optional[int] = None
    vaccinated: Optional[bool] = None
    country: Optional[str] = None
    predicted_breed: Optional[str] = None
    prediction_confidence: Optional[float] = None


class ProductInDB(ProductBase):
    product_id: str = Field(default_factory=lambda: str(uuid4()))
    image: bytes  # Binary data
    date_added: datetime = Field(default_factory=datetime.utcnow)

class ProductRead(ProductBase):
    id: str = Field(alias="_id")
    product_id: str
    date_added: datetime
    has_image: bool

    class Config:
        from_attributes = True
        populate_by_name = True
        # Exclude image from default serialization if it were present, 
        # but we map it to has_image manually or via service
