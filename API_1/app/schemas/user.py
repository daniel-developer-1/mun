from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(default="username", min_length=3)


class UserCreate(UserBase):
    password: str = Field(default="password123", min_length=4, max_length=28)
    email: EmailStr


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
