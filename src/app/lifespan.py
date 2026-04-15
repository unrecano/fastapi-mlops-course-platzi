from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.engine import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
