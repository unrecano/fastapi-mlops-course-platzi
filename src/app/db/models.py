"""
Module to define database models.
"""

from sqlmodel import SQLModel, Field


class PredictionsTickets(SQLModel, table=True):
    """
    Table to store predictions
    """

    id: int | None = Field(default=None, primary_key=True)
    client_name: str
    prediction: str
