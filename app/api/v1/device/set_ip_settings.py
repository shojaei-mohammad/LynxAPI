import subprocess
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import SCRIPTS_PATH
from app.dependencies.token_dependency import get_current_user
from app.schemas.ip_settings import NetworkConfig

router = APIRouter()


def configure_network(
    interface_name: str, ip_address: str, subnet_mask: str, dns_servers: List[str]
):
    # This function will use the `ip` command to set the IP address and subnet mask
    try:
        # Bring the interface down
        subprocess.run(
            ["sudo", "ip", "link", "set", interface_name, "down"], check=True
        )
        # Set the new IP address
        subprocess.run(
            [
                "sudo",
                "ip",
                "addr",
                "add",
                f"{ip_address}/{subnet_mask}",
                "dev",
                interface_name,
            ],
            check=True,
        )
        # Bring the interface up
        subprocess.run(["sudo", "ip", "link", "set", interface_name, "up"], check=True)

        # Clear existing DNS servers and set new ones
        resolv_conf = "\n".join([f"nameserver {dns}" for dns in dns_servers])
        with open("/etc/resolv.conf", "w") as file:
            file.write(resolv_conf)

        return True
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return False


@router.post(
    "/network/{interface_name}/configure",
    summary="Configure Network Interface Settings",
)
async def configure_ip_address(
    interface_name: str,
    config: NetworkConfig,
    current_user: str = Depends(get_current_user),
):
    """
    Configure a network interface with either DHCP or a manual static IP configuration.

    This endpoint allows users to set the network configuration for a specified interface.
    Users can opt for DHCP, which will enable the interface to receive an IP configuration
    dynamically from a DHCP server, or they can choose a manual setup, which requires
    specifying an IP address, subnet mask, and default gateway.

    For a manual configuration, users must provide a valid IPv4 address, subnet mask,
    and optionally a default gateway and DNS server addresses. If DHCP mode is selected,
    these fields should be omitted.

    Parameters:
    - interface_name (str): The name of the network interface to configure (e.g., "eth0").
    - config (NetworkConfig): The configuration details as per the NetworkConfig model.
      This includes the configuration mode, and depending on the mode, the necessary
      IP settings.

    Returns a JSON response indicating the success or failure of the network configuration operation.

    Requires an authorized user context, provided by the `get_current_user` dependency.

    Raises an HTTPException with status code 500 if the configuration fails.
    """

    # Validate mode
    if config.mode not in ["dhcp", "static"]:
        raise HTTPException(status_code=400, detail="Invalid mode specified.")

    # Build the command
    command = ["sudo", SCRIPTS_PATH, interface_name, config.mode]

    if config.mode == "static":
        if not config.ip_address or not config.subnet_prefix or not config.gateway:
            raise HTTPException(
                status_code=400,
                detail="IP address, subnet mask, and gateway are required for manual mode.",
            )
        command.extend(
            [
                str(config.ip_address),
                str(config.subnet_prefix),
                str(config.gateway),
                " ".join([str(dns) for dns in config.dns_servers])
                if config.dns_servers
                else "",
            ]
        )

    # Execute the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check the result
    if result.returncode == 0:
        return {
            "status": f"Network configuration {'automatically' if config.mode == 'dhcp' else 'manually'} updated for "
            f"interface: {interface_name}"
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to update network configuration: " + result.stderr.decode(),
        )
