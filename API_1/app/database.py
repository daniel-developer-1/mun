from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    DATABASE_URL = "postgresql://oferton_user:FHVFDekpxexmJ4fBHPFS6qTzYgXueWjJ@dpg-d76bqe15pdvs739h668g-a.ohio-postgres.render.com/oferton"
    engine = create_engine(DATABASE_URL)
except:
    DATABASE_URL = "sqlite:///./miapi.db"
    engine = create_engine(DATABASE_URL, connect_args={
                           "check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
