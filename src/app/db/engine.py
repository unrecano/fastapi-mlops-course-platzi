"""
Module to create database and tables
"""

from app.settings import settings
from sqlmodel import create_engine, SQLModel, Session

engine = create_engine(settings.db_url, echo=True)


def create_db_and_tables():
    """
    Create database and tables
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Generator for database session to use with Depends()
    """
    with Session(engine) as session:
        yield session
