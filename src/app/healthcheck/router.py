"""
Module to define the healthcheck router.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])


@router.get("")
def healthcheck():
    """
    Endpoint to check the health of the application.
    """
    return {"status": "ok"}
