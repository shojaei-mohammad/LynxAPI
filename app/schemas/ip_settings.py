from ipaddress import IPv4Address, IPv4Network
from typing import List, Optional

from pydantic import BaseModel, Field


class NetworkConfig(BaseModel):
    ip_address: IPv4Address = Field(description="")
    subnet_mask: IPv4Network = Field(description="")
    dns_servers: Optional[List[IPv4Address]] = []
