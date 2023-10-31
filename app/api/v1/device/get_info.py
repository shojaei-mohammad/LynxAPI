import os
import platform
import socket
from datetime import datetime
from fastapi import APIRouter, Depends
from typing import Dict

# If you want more detailed network information
import psutil

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
        "hostname": platform.node(),
        "os": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": " - ".join(platform.architecture()),
        "cpu": platform.processor(),
        "memory": "{:.2f} GB".format(
            os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024.0**3)
        ),
        "ip_address": socket.gethostbyname(socket.gethostname()),  # Get IP Address
        "current_time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # Get current time
        "network_interfaces": {
            interface: address for interface, address in psutil.net_if_addrs().items()
        },  # Get network interfaces
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
