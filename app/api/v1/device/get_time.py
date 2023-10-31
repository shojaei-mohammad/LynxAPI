from fastapi import APIRouter, Depends
from datetime import datetime

from app.dependencies.token_dependency import get_current_user
from app.schemas.info import SystemTimeResponse

router = APIRouter()


def get_system_time() -> datetime:
    """
    Get the current system time.

    Returns:
        datetime: The current system time.
    """
    return datetime.now()


@router.get("/device/clock", response_model=SystemTimeResponse)
async def system_time_info(current_user: str = Depends(get_current_user)) -> dict:
    """
    Endpoint to fetch the system's current time.

    Parameters:
        current_user (str): The authenticated user's name/ID.

    Returns:
        dict: A dictionary containing the system's current time.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    return {"system_time": get_system_time()}
