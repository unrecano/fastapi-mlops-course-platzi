"""
This module contains functions to preprocess text and vectorize it.
"""

from typing import Any

from sklearn.feature_extraction.text import TfidfTransformer
from nltk import word_tokenize
import joblib
import nltk
from nltk.corpus import stopwords
from app.settings import settings
import os

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")

PATH_PIKL = os.path.join(settings.models_path, "count_vectorizer.pkl")

stop_words = set(stopwords.words("english"))

count_vectorizer = joblib.load(PATH_PIKL)


def tokenize_text(text: str) -> list[str]:
    """
    Tokenize text with NLTK

    Args:
        text (str): Text to tokenize

    Return:
        list[str]: List of tokens
    """
    return word_tokenize(text.lower())


def remove_stopwords(tokens: list[str]) -> list[str]:
    """
    Remove stopwords from tokens

    Args:
        tokens (list[str]): List of tokens

    Return:
        list[str]: List of tokens without stopwords
    """
    return [token for token in tokens if token.lower() not in stop_words]


def pos_tagging(tokens: list[str]) -> str:
    """
    POS tagging of tokens

    Args:
        tokens (list[str]): List of tokens

    Return:
        str: String of nouns
    """
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tagged if pos.startswith("NN")]
    return " ".join(nouns)


def vectorize_text(text: str) -> Any:
    """
    Vectorize text with model

    Args:
        text (str): Text to vectorize

    Return:
        Any: Vectorized text
    """
    X_vectorized = count_vectorizer.transform([text])
    tfidf_transformer = TfidfTransformer()
    tfidf_matrix = tfidf_transformer.fit_transform(X_vectorized)
    return tfidf_matrix


def preprocess_text(text: str) -> Any:
    """
    Preprocess text with NLTK

    Args:
        text (str): Text to preprocess

    Return:
        Any: Preprocessed text
    """
    tokens = tokenize_text(text)
    tokens_without_stopwords = remove_stopwords(tokens)
    nouns = pos_tagging(tokens_without_stopwords)
    X_vectorized = vectorize_text(nouns)
    return X_vectorized


def run_preprocess_text(text: str) -> Any:
    """
    Run preprocess text

    Args:
        text (str): Text to preprocess

    Return:
        Any: Preprocessed text
    """
    return preprocess_text(text)
