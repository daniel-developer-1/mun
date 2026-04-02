from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
try:
    from ..crud.user import get_user_by_id, get_users, create_user
    from ..schemas.user import UserCreate, UserResponse
    from ..models.user import User
    from ..database import get_db
except:

    from crud.user import get_user_by_id, get_users, create_user
    from schemas.user import UserCreate, UserResponse
    from models.user import User
    from database import get_db


router = APIRouter()


@router.post("/create_user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return new_user


@router.get("/get_users", response_model=List[UserResponse])
def get_all_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return get_users(db, skip, limit)
