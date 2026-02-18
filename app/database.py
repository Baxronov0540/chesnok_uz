from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from fastapi import Depends
from app.config import settings

DB_URL = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)


class Base(DeclarativeBase):
    pass


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


db_deb = Annotated[Session, Depends(get_db)]
