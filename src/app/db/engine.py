"""
Module to create database and tables
"""

from app.settings import settings
from sqlmodel import create_engine, SQLModel

engine = create_engine(settings.db_url, echo=True)


def create_db_and_tables():
    """
    Create database and tables
    """
    SQLModel.metadata.create_all(engine)
