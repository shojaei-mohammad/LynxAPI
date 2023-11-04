import os

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.token_dependency import get_current_user
from app.schemas.ip_settings import NetworkConfig

router = APIRouter()


def set_static_ip(interface_name, ip_address, subnet_mask, dns_servers=[]):
    backup_cmd = "sudo cp /etc/network/interfaces /etc/network/interfaces.backup"
    os.system(backup_cmd)

    config_lines = [
        f"auto {interface_name}",
        f"iface {interface_name} inet static",
        f"address {ip_address}",
        f"netmask {subnet_mask}",
    ]

    # Remove existing configuration for the interface
    with open("/etc/network/interfaces", "r") as f:
        lines = f.readlines()
    with open("/etc/network/interfaces", "w") as f:
        for line in lines:
            if (
                line.strip() != f"auto {interface_name}"
                and line.strip() != f"iface {interface_name} inet static"
            ):
                f.write(line)

    # Update /etc/network/interfaces with the new config
    with open("/etc/network/interfaces", "a") as f:
        f.write("\n".join(config_lines))

    # If DNS servers are provided, update /etc/resolv.conf
    if dns_servers:
        with open("/etc/resolv.conf", "w") as f:
            for dns in dns_servers:
                f.write(f"nameserver {dns}\n")

    # Restart networking service to apply changes
    os.system("sudo /etc/init.d/networking restart")


@router.post("/update-network-config/{interface_name}/")
async def update_network_config(
    interface_name: str,
    config: NetworkConfig,
    current_user: str = Depends(get_current_user),
):
    try:
        set_static_ip(
            interface_name, config.ip_address, config.subnet_mask, config.dns_servers
        )
        return {
            "status": "success",
            "message": f"Network configuration updated successfully for {interface_name}",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
