from typing import Dict, Any

from pydantic import BaseModel, Field


class SystemInfoResponse(BaseModel):
    hostname: str = Field(
        description="The name assigned to the system, often used to identify it on a network."
    )
    os: str = Field(description="The operating system name running on the system.")
    release: str = Field(description="The release version of the operating system.")
    version: str = Field(
        description="Detailed version information of the operating system, which might include patch or update levels."
    )
    architecture: str = Field(
        description="The system's CPU architecture, such as x86, x86_64, arm, etc."
    )
    cpu: str = Field(
        description="Information about the system's central processing unit, including its make and model."
    )
    memory: str = Field(
        description="Information about the system's memory configuration, including total available memory and its "
        "type."
    )
    ip_address: str = Field(
        description="The primary IP address assigned to the system."
    )
    current_time: str = Field(description="The current system time in string format.")
    network_interfaces: Dict[str, Any] = Field(
        description="A dictionary where keys are the names of network interfaces on the system (e.g., eth0, wlan0), "
        "and values provide detailed address information for each interface."
    )


class HostnameResponse(BaseModel):
    hostname: str = Field(
        description="The name assigned to the system. This is often used to identify the system on a network."
    )


class TimeDetails(BaseModel):
    Time: str = Field(description="The current time on the system, in HH:MM:SS format.")
    Date: str = Field(
        description="The current date on the system, in YYYY-MM-DD format."
    )
    Zone: str = Field(description="The current timezone of the system.")
