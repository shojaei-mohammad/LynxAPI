from pydantic import BaseModel, Field


class Hostname(BaseModel):
    hostname: str = Field(
        ..., example="new-hostname", description="The desired hostname for the system."
    )
