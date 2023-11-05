from pydantic import BaseModel, Field


class SystemResources(BaseModel):
    """
    System Resources Data Model

    Represents the system's resource usage in terms of CPU, memory, and disk.
    The usage is given as a percentage of the total capacity.
    """

    cpu_usage_percent: float = Field(
        ...,
        title="CPU Usage Percentage",
        description="The percentage of CPU utilization.",
        example=55.5,
        gt=0,
        lt=100,
        units="%",
    )

    memory_usage_percent: float = Field(
        ...,
        title="Memory Usage Percentage",
        description="The percentage of memory (RAM) utilization.",
        example=70.3,
        gt=0,
        lt=100,
        units="%",
    )

    disk_usage_percent: float = Field(
        ...,
        title="Disk Usage Percentage",
        description="The percentage of disk space utilization on the root partition.",
        example=82.2,
        gt=0,
        lt=100,
        units="%",
    )
