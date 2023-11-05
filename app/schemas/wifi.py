from pydantic import BaseModel, Field


class WiFiConfig(BaseModel):
    ssid: str = Field(..., title="SSID", description="The name of the Wi-Fi network.")
    password: str = Field(
        ..., title="Password", description="The password for the Wi-Fi network."
    )
