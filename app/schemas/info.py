from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class SystemInfoResponse(BaseModel):
    hostname: str
    os: str
    release: str
    version: str
    architecture: str
    cpu: str
    memory: str
    ip_address: str
    current_time: str
    network_interfaces: Dict[
        str, Any
    ]  # Using a Dict to represent interface name as key and its address details as value


class HostnameResponse(BaseModel):
    hostname: str


class SystemTimeResponse(BaseModel):
    system_time: datetime
