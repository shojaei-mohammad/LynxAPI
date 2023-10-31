import platform
from fastapi import APIRouter, Depends

from app.dependencies.token_dependency import get_current_user
from app.schemas.info import HostnameResponse

router = APIRouter()


def fetch_hostname() -> str:
    """
    Get the system hostname.

    Returns:
        str: The system hostname.
    """
    return platform.node()


@router.get("/device/hostname", response_model=HostnameResponse)
async def hostname_info(current_user: str = Depends(get_current_user)) -> dict:
    """
    Endpoint to fetch the system's hostname.

    Parameters:
        current_user (str): The authenticated user's name/ID.

    Returns:
        dict: A dictionary containing the system's hostname.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    return {"hostname": fetch_hostname()}
