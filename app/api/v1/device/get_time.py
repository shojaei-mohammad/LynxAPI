import subprocess
from datetime import datetime

import pytz
from fastapi import APIRouter, Depends

from app.dependencies.token_dependency import get_current_user
from app.schemas.info import TimeDetails

router = APIRouter()


def get_system_timezone() -> str:
    try:
        # Get the current timezone from the system settings
        result = subprocess.run(["timedatectl", "show", "-p", "Timezone", "--value"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "Unknown"
    except Exception as e:
        print(f"Error getting system timezone: {e}")
        return "Unknown"


def get_system_time_details() -> dict:
    """
    Get the current system time details including time, date, and timezone.

    Returns:
        dict: A dictionary containing the system's current time details.
    """
    system_tz_name = get_system_timezone()
    local_tz = pytz.timezone(system_tz_name)

    current_time = datetime.now(local_tz)
    time_str = current_time.strftime("%H:%M:%S")
    date_str = current_time.strftime("%Y-%m-%d")
    offset_str = f"{current_time.utcoffset().total_seconds() / 3600:+05.2f}".replace(".", ":")
    tz_string = f"{local_tz.zone} ({offset_str})"

    return {"Time": time_str, "Date": date_str, "Zone": tz_string}


@router.get(
    "/device/clock",
    response_model=TimeDetails,
    summary="Get system datatime and timezone",
)
async def system_time_info(current_user: str = Depends(get_current_user)) -> TimeDetails:
    """
    Endpoint to fetch the system's current time details.

    Parameters:
        current_user (str): The authenticated user's name/ID.

    Returns:
        TimeDetails: An object containing the system's current time details.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    return get_system_time_details()
