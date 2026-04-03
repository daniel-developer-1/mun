from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(default="name", min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(
        default="password123",
        min_length=4,
        max_length=50
    )
    email: EmailStr


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
