import os
from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI

from app.db.engine import create_db_and_tables
from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()

    # Load ML models into application state
    model_path = os.path.join(settings.models_path, "model.pkl")
    count_vec_path = os.path.join(settings.models_path, "count_vectorizer.pkl")

    app.state.model = joblib.load(model_path)
    app.state.count_vectorizer = joblib.load(count_vec_path)

    yield

    # Clean up state on shutdown
    app.state.model = None
    app.state.count_vectorizer = None
