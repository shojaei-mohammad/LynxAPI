import subprocess

from fastapi import APIRouter, HTTPException, Depends

from app.dependencies.token_dependency import get_current_user
from app.schemas.hostname import Hostname

router = APIRouter()


def update_hostname(hostname: str) -> bool:
    try:
        subprocess.run(["hostnamectl", "set-hostname", hostname], check=True)
        return True
    except Exception as e:
        print(f"Error setting hostname: {e}")
        return False


@router.post("/set_hostname/", summary="Configure hostname")
async def set_hostname_endpoint(
    hostname_data: Hostname, current_user: str = Depends(get_current_user)
):
    """
    Update the system's hostname.

    This endpoint allows authorized users to update the system's current hostname
    to the provided value.

    Args:
        hostname_data (Hostname): A Pydantic model that captures the desired hostname.

    Returns:
        dict: A dictionary with a status key indicating the success or failure of the hostname update.

    Raises:
        HTTPException: If there's an error updating the hostname.
        :param hostname_data:
        :param current_user:
    """
    result = update_hostname(hostname_data.hostname)
    if result:
        return {"status": "Hostname updated successfully!"}
    else:
        raise HTTPException(status_code=500, detail="Error updating hostname.")
