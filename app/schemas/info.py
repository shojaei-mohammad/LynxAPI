from pydantic import BaseModel


class SystemInfoResponse(BaseModel):
    hostname: str
    os: str
    release: str
    version: str
    architecture: str
    cpu: str
    memory: str
