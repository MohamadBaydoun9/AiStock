from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "user"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    user_id: str = Field(default_factory=lambda: str(uuid4()))
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserRead(UserBase):
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True
