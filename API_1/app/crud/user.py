from fastapi import HTTPException, status
try:

    from ..models.user import User
    from ..schemas.user import UserCreate
except:
    from models.user import User
    from schemas.user import UserCreate
from sqlalchemy.orm import Session


def create_user(db: Session, user: UserCreate):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
