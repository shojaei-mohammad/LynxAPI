from pydantic import BaseModel
from typing import List, Dict, Optional


class InterfaceAddress(BaseModel):
    family: str
    address: str
    netmask: Optional[str] = None
    broadcast: Optional[str] = None
    ptp: Optional[str] = None


class InterfaceStat(BaseModel):
    speed: int
    duplex: str
    mtu: int
    isup: bool


class InterfaceDetail(BaseModel):
    addresses: List[InterfaceAddress]
    stats: InterfaceStat


class InterfacesResponse(BaseModel):
    interfaces: Dict[str, InterfaceDetail]


class InterfaceRequest(BaseModel):
    interface_name: str
