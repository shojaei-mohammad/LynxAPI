import psutil
from fastapi import APIRouter, Depends

from app.dependencies.token_dependency import get_current_user
from app.schemas.system_resources import SystemResources

# Create a new API router instance to handle routes related to system resources.
router = APIRouter()


@router.get(
    "/system-resources", response_model=SystemResources, summary="Get system resources"
)
# Define an endpoint that retrieves the system's current resource usage.
# It requires a current user dependency which is resolved by the get_current_user function.
# The endpoint will return data conforming to the SystemResources model.
async def get_system_resources_endpoint(current_user: str = Depends(get_current_user)):
    """
    Get system resource utilization details.

    This endpoint requires user authentication. Upon successful authentication,
    it retrieves and returns the system's CPU usage, memory usage, and disk usage
    as a percentage of their total capacities.

    Args:
        current_user (str): The username of the authenticated user, obtained from the token dependency.

    Returns:
        SystemResources: An object containing the system's resource utilization details,
                         including CPU, memory, and disk usage percentages.
    """

    # Get the current CPU usage as a percentage.
    cpu_usage_percent = psutil.cpu_percent()

    # Get the current memory usage as a percentage.
    memory_usage_percent = psutil.virtual_memory().percent

    # Get the current disk usage as a percentage.
    # This specifically checks the root partition '/'.
    disk_usage_percent = psutil.disk_usage("/").percent

    # Return the gathered resource information packaged in a SystemResources response model.
    return SystemResources(
        cpu_usage_percent=cpu_usage_percent,
        memory_usage_percent=memory_usage_percent,
        disk_usage_percent=disk_usage_percent,
    )
