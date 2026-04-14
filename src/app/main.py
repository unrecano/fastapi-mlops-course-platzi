from fastapi import FastAPI

from app.lifespan import lifespan
from app.healthcheck.router import router as healthcheck_router
from app.predicts.router import router as predicts_router


app = FastAPI(
    title="Sentiment Analysis API",
    description="Sentiment Analysis API",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(healthcheck_router)
app.include_router(predicts_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
