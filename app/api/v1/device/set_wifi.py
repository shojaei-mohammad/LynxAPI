import shlex
import subprocess

from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies.token_dependency import get_current_user
from app.schemas.wifi import WiFiConfig

router = APIRouter()


def set_wifi_connection(ssid: str, password: str) -> bool:
    # Using 'nmcli' to connect to a Wi-Fi network
    command = (
        f"nmcli dev wifi connect {shlex.quote(ssid)} password {shlex.quote(password)}"
    )

    try:
        # Execute the command without using shell=True for security reasons
        subprocess.run(
            shlex.split(command),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting Wi-Fi: {e.stderr.decode().strip()}")
        return False


@router.post("/wifi-setup", summary="Configure wifi connection")
async def setup_wifi(config: WiFiConfig, current_user: str = Depends(get_current_user)):
    try:
        # Here you would include the logic to set up the Wi-Fi connection using the provided details.
        # This is highly platform-dependent and might require invoking system commands or using a
        # platform-specific library.
        success = True  # Placeholder for actual connection logic
        if success:
            return {"message": "Wi-Fi connection successfully established."}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to establish Wi-Fi connection.",
            )
    except Exception as e:
        # In case of an exception, return an error response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
