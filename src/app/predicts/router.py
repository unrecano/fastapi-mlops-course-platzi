"""
Module to define the predicts router.
"""

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.engine import get_session
from app.predicts.services import make_predictions

router = APIRouter(prefix="/predicts", tags=["Predicts"])


class Sentence(BaseModel):
    client_name: str
    text: str


class ProcessTextRequestModel(BaseModel):
    sentences: list[Sentence]


@router.post("")
async def predict(
    payload: ProcessTextRequestModel,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """
    Predict the sentiment of the text

    Args:
        payload (ProcessTextRequestModel): Request model
        request (Request): FastAPI request object

    Return:
        dict: Dictionary with the predicted sentiment
    """
    model = request.app.state.model
    count_vectorizer = request.app.state.count_vectorizer
    predictions = await make_predictions(
        payload.sentences, session, model, count_vectorizer
    )
    return {"predictions": predictions}
