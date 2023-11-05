from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class InterfaceAddress(BaseModel):
    family: str = Field(description="The family of the address, such as IPv4 or IPv6.")
    address: str = Field(
        description="The IP address associated with the network interface."
    )
    netmask: Optional[str] = Field(
        default=None, description="The subnet mask associated with the IP address."
    )
    broadcast: Optional[str] = Field(
        default=None,
        description="The broadcast address associated with the network interface.",
    )
    ptp: Optional[str] = Field(
        default=None,
        description="Point-to-Point Protocol address for the interface, if applicable.",
    )


class InterfaceStat(BaseModel):
    speed: int = Field(
        description="The speed of the network interface in Mbps (Megabits per second)."
    )
    duplex: str = Field(
        description="The duplex mode of the interface, indicating if it can send and receive data simultaneously. "
        "Typical values are 'full' or 'half'."
    )
    mtu: int = Field(
        description="Maximum Transmission Unit. Represents the size of the largest packet that the interface can "
        "transmit."
    )
    isup: bool = Field(
        description="A boolean value indicating if the interface is up (active) or down (inactive)."
    )


class InterfaceDetail(BaseModel):
    addresses: List[InterfaceAddress] = Field(
        description="A list of address objects associated with the network interface."
    )
    stats: InterfaceStat = Field(
        description="Statistics and status details for the network interface."
    )


class InterfacesResponse(BaseModel):
    interfaces: Dict[str, InterfaceDetail] = Field(
        description="A dictionary where keys are the names of network interfaces on the system (e.g., eth0, wlan0), "
        "and values provide detailed address and status information for each interface."
    )


class InterfaceRequest(BaseModel):
    interface_name: str = Field(
        description="The name of a specific network interface (e.g., eth0, wlan0) for which details are being "
        "requested."
    )
