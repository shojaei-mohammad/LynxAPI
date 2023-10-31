from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from subprocess import run, CalledProcessError
from app.dependencies.token_dependency import get_current_user
from app.schemas.set_hostname import (
    SetHostnameRequest,
)  # Assuming you've saved the model in this location

router = APIRouter()


def set_system_hostname(new_hostname: str) -> None:
    """
    Set system hostname.

    Parameters:
        new_hostname (str): The new hostname to be set.

    Raises:
        Exception: If there's an error setting the hostname.
    """
    try:
        result = run(
            ["sudo", "hostnamectl", "set-hostname", new_hostname],
            capture_output=True,
            text=True,
            check=True,
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
    except CalledProcessError as e:
        raise Exception(e.stderr)


@router.post("/device/set-hostname")
async def set_device_hostname(
    request: SetHostnameRequest, current_user: str = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Endpoint to set the device's hostname.

    Parameters:
        request (SetHostnameRequest): Contains the new hostname to be set.
        user (str, optional): The authenticated user's name/ID. Defaults to Depends on(verify_token).

    Returns:
        dict: A dictionary confirming the change.

    Raises:
        HTTPException: If the user is not authenticated or if there's an error setting the hostname.
        :param request:
        :param current_user:
    """

    # Check if the user has the necessary privileges. This is a basic example; you might have more complex logic.
    if not current_user == "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        set_system_hostname(request.hostname)
        return {"status": "success", "message": f"Hostname set to {request.hostname}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
