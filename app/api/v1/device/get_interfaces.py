import psutil
from fastapi import APIRouter, Depends

from app.dependencies.token_dependency import get_current_user
from app.schemas.interfaces import InterfacesResponse

router = APIRouter()


def get_interfaces_info() -> dict:
    """
    Get information about all available network interfaces using psutil.

    Returns:
        dict: A dictionary containing details for each network interface.
    """
    interfaces_info = {}
    for interface, addrs in psutil.net_if_addrs().items():
        addresses = []
        for addr in addrs:
            addresses.append(
                {
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast,
                    "ptp": addr.ptp,
                }
            )

        stats = psutil.net_if_stats()[interface]
        stats_detail = {
            "speed": stats.speed,
            "duplex": str(stats.duplex),
            "mtu": stats.mtu,
            "isup": stats.isup,
        }

        interfaces_info[interface] = {"addresses": addresses, "stats": stats_detail}

    return interfaces_info


@router.get(
    "/device/interfaces",
    response_model=InterfacesResponse,
    summary="Get all available interfaces",
)
async def interfaces_info(current_user: str = Depends(get_current_user)) -> dict:
    """
    Endpoint to fetch information about all available network interfaces using psutil.

    Parameters:
        current_user (str): The authenticated user's name/ID.

    Returns:
        dict: A dictionary containing details for each network interface.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    return {"interfaces": get_interfaces_info()}
