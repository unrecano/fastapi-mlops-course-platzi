from unittest.mock import MagicMock, patch

from app.predicts.router import Sentence
from app.predicts.services import run_model_inference


@patch("app.predicts.services.preprocess_text")
def test_run_model_inference(mock_preprocess_text):
    # Setup
    mock_matrix = MagicMock()
    mock_matrix.toarray.return_value = [[0.1, 0.2]]
    mock_preprocess_text.return_value = [mock_matrix]

    mock_model = MagicMock()
    mock_model.predict.return_value = [0]  # 0 maps to "Bank Account Services"

    mock_vectorizer = MagicMock()

    sentences = [
        Sentence(client_name="John Doe", text="I need help with my checking account")
    ]

    # Execute
    predictions = run_model_inference(sentences, mock_model, mock_vectorizer)

    # Assert
    assert len(predictions) == 1
    assert predictions[0]["client_name"] == "John Doe"
    assert predictions[0]["prediction"] == "Bank Account Services"

    mock_preprocess_text.assert_called_once()
    mock_model.predict.assert_called_once()
