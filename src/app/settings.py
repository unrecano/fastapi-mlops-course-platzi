"""
Module to manage application settings.
"""

import pathlib

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the application
    """

    db_url: str = Field(..., alias="DATABASE_URL")
    models_path: str = str(pathlib.Path(__file__).parent.parent.parent / "models")


# Instance of settings
settings = Settings()
