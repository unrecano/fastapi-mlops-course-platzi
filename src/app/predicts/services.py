import numpy as np
from utils import preprocess_text
import joblib
from sqlmodel import Session
from app.db.models import PredictionsTickets
from app.settings import settings
import os

label_mapping = {
    "0": "Bank Account Services",
    "1": "Credit Report or Repaid Card",
    "2": "Mortgage/Loan",
}


def make_predictions(sentences: list, session: Session) -> list:
    """
    Make predictions and save them to the database.

    Args:
        sentences (list): List of sentences to predict
        session (Session): Session to use for database operations

    Return:
        list: List of predictions
    """
    model_path = os.path.join(settings.models_path, "model.pkl")
    model = joblib.load(model_path)
    predictions = []

    for sentence in sentences:
        process_data_vectorized = preprocess_text(sentence.text)
        X_dense = [sparse_matrix.toarray() for sparse_matrix in process_data_vectorized]
        X_dense = np.vstack(X_dense)
        preds = model.predict(X_dense)
        decoded_prediction = label_mapping[str(preds[0])]

        prediction_ticket = PredictionsTickets(
            client_name=sentence.client_name,
            prediction=decoded_prediction,
        )

        predictions.append(
            {
                "client_name": sentence.client_name,
                "prediction": decoded_prediction,
            }
        )

        session.add(prediction_ticket)

    session.commit()
    if sentences:
        session.refresh(prediction_ticket)

    return predictions
