# app/api/v1/device/get_info.py

import os
import platform
from fastapi import APIRouter, Depends
from typing import Dict

from app.dependencies.token_dependency import get_current_user
from app.schemas.info import SystemInfoResponse

router = APIRouter()


def get_device_info() -> Dict[str, str]:
    """
    Get general information of the device.

    Returns:
        dict: A dictionary containing general device information such as hostname, os, release, etc.
    """
    info = {
        "hostname": platform.node(),  # Get device hostname
        "os": platform.system(),  # Get operating system
        "release": platform.release(),  # Get OS release
        "version": platform.version(),  # Get OS version
        "architecture": " - ".join(platform.architecture()),  # Get OS architecture
        "cpu": platform.processor(),  # Get CPU details
        "memory": "{:.2f} GB".format(
            os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024.0**3)
        ),  # Calculate memory in GB and format it as string
    }
    return info


@router.get("/device/info", response_model=SystemInfoResponse)
async def device_info(current_user: str = Depends(get_current_user)) -> Dict[str, str]:
    """
    Endpoint to fetch the device's general information.

    Parameters:
        user (str, optional): The authenticated user's name/ID. Defaults to Depends on(verify_token).

    Returns:
        dict: A dictionary containing the device's general information.

    Raises:
        HTTPException: If the user is not authenticated.
        :param current_user:
    """

    return get_device_info()
