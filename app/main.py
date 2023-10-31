from fastapi import FastAPI
import uvicorn
from app.api.v1.admin import authorization
from app.api.v1 import device
from app.middleware.check_token import JWTTokenMiddleware


app = FastAPI(
    title="RasAPI Documentation",
    description="A comprehensive API service for managing devices, with secure admin authorization capabilities.",
    version="1.0.0",
    openapi_tags=[],  # your tags if any
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(JWTTokenMiddleware)

app.include_router(authorization.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(device.get_info.router, prefix="/api/v1", tags=["core"])
app.include_router(device.get_hostname.router, prefix="/api/v1", tags=["core"])
app.include_router(device.get_time.router, prefix="/api/v1", tags=["core"])
app.include_router(device.get_interfaces.router, prefix="/api/v1", tags=["core"])
app.include_router(device.get_interface_by_name.router, prefix="/api/v1", tags=["core"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)


if __name__ == "__main__":
    main()
