"""
Module to create database and tables
"""

from app.settings import settings
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

async_db_url = settings.db_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(async_db_url, echo=True)


async def create_db_and_tables():
    """
    Create database and tables asynchronously
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """
    Generator for async database session to use with Depends()
    """
    async with AsyncSession(engine) as session:
        yield session
