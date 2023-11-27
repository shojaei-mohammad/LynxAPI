import subprocess

from fastapi import APIRouter, HTTPException, Depends

from app.dependencies.token_dependency import get_current_user
from app.schemas.timezone import Timezone

router = APIRouter()


def update_timezone(timezone: str) -> bool:
    try:
        # Set the new timezone
        subprocess.run(["timedatectl", "set-timezone", timezone], check=True)

        return True
    except Exception as e:
        print(f"Error updating timezone or restarting clock service: {e}")
        return False


@router.post("/set_timezone/", summary="Configure time zone")
async def set_timezone_endpoint(
    timezone_data: Timezone, current_user: str = Depends(get_current_user)
):
    """
    Update the system's timezone.

    This endpoint allows authorized users to update the system's current timezone
    based on the provided timezone format 'Region/City', such as 'Asia/Tehran'.

    Args:
        timezone_data (Timezone): A Pydantic model that captures the desired timezone.
        current_user (str): The currently authenticated user, determined through dependency injection.

    Returns:
        dict: A dictionary with a status key indicating the success or failure of the timezone update.

    Raises:
        HTTPException: If there's an error updating the timezone.
    """
    # Logic to set the timezone goes here
    result = update_timezone(timezone_data.timezone)
    if result:
        return {"status": "Timezone updated successfully!"}
    else:
        raise HTTPException(status_code=500, detail="Error updating timezone.")
