"""
Module to define the predicts router.
"""

from fastapi import APIRouter
from sqlmodel import Session
from pydantic import BaseModel
from app.db.engine import engine
from app.predicts.services import make_predictions

router = APIRouter(prefix="/predicts", tags=["Predicts"])


class Sentence(BaseModel):
    client_name: str
    text: str


class ProcessTextRequestModel(BaseModel):
    sentences: list[Sentence]


@router.post("")
async def predict(request: ProcessTextRequestModel):
    """
    Predict the sentiment of the text

    Args:
        request (ProcessTextRequestModel): Request model

    Return:
        dict: Dictionary with the predicted sentiment
    """
    session = Session(engine)
    predictions = make_predictions(request.sentences, session)
    return {"predictions": predictions}
