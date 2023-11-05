import psutil
from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.token_dependency import get_current_user
from app.schemas.interfaces import InterfaceDetail

router = APIRouter()


def get_interface_detail_by_name(interface_name: str) -> dict:
    """
    Get information about a specific network interface using psutil.

    Args:
        interface_name (str): The name of the interface.

    Returns:
        dict: A dictionary containing details for the specified network interface.
    """
    addrs = psutil.net_if_addrs().get(interface_name)
    if not addrs:
        raise HTTPException(status_code=404, detail="Interface not found")

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

    stats = psutil.net_if_stats().get(interface_name)
    stats_detail = {
        "speed": stats.speed,
        "duplex": str(stats.duplex),
        "mtu": stats.mtu,
        "isup": stats.isup,
    }

    return {"addresses": addresses, "stats": stats_detail}


@router.get(
    "/device/interface/{interface_name}",
    response_model=InterfaceDetail,
    summary="Get interface detail by interaface name",
)
async def interface_info_by_name(
    interface_name: str, current_user: str = Depends(get_current_user)
) -> dict:
    """
    Endpoint to fetch information about a specific network interface using psutil.

    Parameters:
        interface_name (str): The name of the interface.
        current_user (str): The authenticated user's name/ID.

    Returns:
        dict: A dictionary containing details for the specified network interface.

    Raises:
        HTTPException: If the interface is not found or the user is not authenticated.
    """
    return get_interface_detail_by_name(interface_name)
