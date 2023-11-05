from ipaddress import IPv4Address
from typing import List, Optional

from pydantic import BaseModel, Field


class NetworkConfig(BaseModel):
    mode: str = Field(
        ...,
        description="The mode of network configuration, 'dhcp' for dynamic configuration or 'static' for manual "
        "configuration.",
        examples=["dhcp", "static"],
    )
    ip_address: Optional[IPv4Address] = Field(
        None,
        description="The IPv4 address to assign to the network interface for static configuration.",
        examples=["192.168.1.100"],
    )
    subnet_prefix: Optional[int] = Field(
        None,
        description="The subnet prefix length for the network interface for static configuration.",
        examples=[24],
        ge=0,  # Greater than or equal to 0
        le=32,  # Less than or equal to 32
    )
    gateway: Optional[IPv4Address] = Field(
        None,
        description="The default gateway IPv4 address for the network interface for static configuration.",
        examples=["192.168.1.1"],
    )
    dns_servers: Optional[List[IPv4Address]] = Field(
        None,
        description="A list of DNS server IPv4 addresses for the network interface, for both static and DHCP modes.",
        examples=["['8.8.8.8' , '4.2.24']"],
    )
