from sqlmodel import (
    SQLModel,
    create_engine,
    Session
)

from app.core.config import config


engine = create_engine(
    config.DATABASE_URL,
    echo=False
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)