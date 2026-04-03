from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.user import get_users, create_user
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.database import get_db
from app.utils.auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_root():
    return {"Message": "Welcome to my API"}


@router.post("/create_user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = create_user(db, user)
    return new_user


@router.get("/get_users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Solo usuarios autenticados pueden ver la lista de usuarios"""
    return get_users(db, skip, limit)


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtiene el perfil del usuario autenticado"""
    return current_user
