import numpy as np
from typing import Any
from .utils import preprocess_text
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.concurrency import run_in_threadpool
from app.db.models import PredictionsTickets

label_mapping = {
    "0": "Bank Account Services",
    "1": "Credit Report or Repaid Card",
    "2": "Mortgage/Loan",
}


def run_model_inference(sentences: list, model: Any, count_vectorizer: Any) -> list:
    """
    Run model inference

    Args:
        sentences (list): List of sentences to predict
        model (Any): The preloaded ML model
        count_vectorizer (Any): The preloaded CountVectorizer

    Return:
        list: List of predictions
    """
    predictions = []
    for sentence in sentences:
        process_data_vectorized = preprocess_text(
            sentence.text, vectorizer=count_vectorizer
        )
        X_dense = [sparse_matrix.toarray() for sparse_matrix in process_data_vectorized]
        X_dense = np.vstack(X_dense)
        preds = model.predict(X_dense)
        decoded_prediction = label_mapping[str(preds[0])]

        predictions.append(
            {
                "client_name": sentence.client_name,
                "prediction": decoded_prediction,
            }
        )
    return predictions


async def make_predictions(
    sentences: list, session: AsyncSession, model: Any, count_vectorizer: Any
) -> list:
    """
    Make predictions and save them to the database asynchronously.

    Args:
        sentences (list): List of sentences to predict
        session (AsyncSession): Session to use for database operations
        model (Any): The preloaded ML model
        count_vectorizer (Any): The preloaded CountVectorizer

    Return:
        list: List of predictions
    """
    predictions = await run_in_threadpool(
        run_model_inference, sentences, model, count_vectorizer
    )

    for item in predictions:
        prediction_ticket = PredictionsTickets(
            client_name=item["client_name"],
            prediction=item["prediction"],
        )
        session.add(prediction_ticket)

    await session.commit()

    return predictions
