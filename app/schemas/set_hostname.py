from pydantic import BaseModel


class SetHostnameRequest(BaseModel):
    hostname: str

    class Config:
        schema_extra = {
            "example": {
                "hostname": "new-hostname",
            }
        }
