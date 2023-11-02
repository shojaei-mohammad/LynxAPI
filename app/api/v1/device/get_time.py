from datetime import datetime

import pytz
from fastapi import APIRouter, Depends

from app.dependencies.token_dependency import get_current_user
from app.schemas.info import TimeDetails

router = APIRouter()


def get_system_time_details() -> dict:
    """
    Get the current system time details including time, date, and timezone.

    Returns:
        dict: A dictionary containing the system's current time details.
    """
    current_time = datetime.now()
    local_offset = current_time.astimezone().utcoffset().total_seconds() / 3600
    local_tz_name = next(
        (
            tz
            for tz in pytz.all_timezones
            if datetime.now(pytz.timezone(tz)).utcoffset().total_seconds() / 3600
            == local_offset
        ),
        "Unknown",
    )
    local_tz = pytz.timezone(local_tz_name)

    current_time = datetime.now(local_tz)
    time_str = current_time.strftime("%H:%M:%S")
    date_str = current_time.strftime("%Y-%m-%d")
    offset_str = f"{local_offset:+05.2f}".replace(".", ":")
    tz_string = f"{local_tz.zone} ({offset_str})"

    return {"Time": time_str, "Date": date_str, "Zone": tz_string}


@router.get("/device/clock", response_model=TimeDetails)
async def system_time_info(current_user: str = Depends(get_current_user)) -> dict:
    """
    Endpoint to fetch the system's current time details.

    Parameters:
        current_user (str): The authenticated user's name/ID.

    Returns:
        dict: A dictionary containing the system's current time details.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    return get_system_time_details()
