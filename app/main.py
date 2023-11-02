import uvicorn
from fastapi import HTTPException, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError

from app.api.v1 import device
from app.api.v1.admin import authorization
from app.core.config import DOCS
from app.middleware.check_token import JWTTokenMiddleware

app = FastAPI(
    title="RasAPI Documentation",
    description="A comprehensive API service for managing devices, with secure admin authorization capabilities.",
    version="1.0.0",
    openapi_tags=[],  # your tags if any
    openapi_url="/openapi.json",
    docs_url="/docs" if DOCS else None,
    redoc_url="/redoc" if DOCS else None,
)


app.add_middleware(JWTTokenMiddleware)

app.include_router(authorization.router, prefix="/api/admin", tags=["admin"])
app.include_router(device.get_info.router, prefix="/api", tags=["core"])
app.include_router(device.get_hostname.router, prefix="/api", tags=["core"])
app.include_router(device.get_time.router, prefix="/api", tags=["core"])
app.include_router(device.get_interfaces.router, prefix="/api", tags=["core"])
app.include_router(device.get_interface_by_name.router, prefix="/api", tags=["core"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(DBAPIError)
async def sqlalchemy_exception_handler(request, exc: DBAPIError):
    return JSONResponse(
        status_code=400,
        content={"message": "An error occurred with the database."},
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)


if __name__ == "__main__":
    main()
