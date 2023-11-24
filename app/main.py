import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError
from starlette.requests import Request

from app.api.v1 import device
from app.api.v1.admin import authorization
from app.core.config import DOCS, UVICORN_HOST, UVICORN_PORT
from app.middleware.check_token import JWTTokenMiddleware
from app.utils.logger import configure_logger

# Configure the logger for the application
logger = configure_logger()

# Initialize the FastAPI application with metadata
app = FastAPI(
    title="RasAPI Documentation",
    description="A comprehensive API service for managing devices, with secure admin authorization capabilities.",
    version="1.0.0",
    openapi_tags=[],  # Replace with your tags if any
    openapi_url="/openapi.json",
    docs_url="/docs" if DOCS else None,
    redoc_url="/redoc" if DOCS else None,
)

# Add JWT Token Middleware to the application
app.add_middleware(JWTTokenMiddleware)

# Include the API routers from different modules
app.include_router(authorization.router, prefix="/api/admin", tags=["admin"])
app.include_router(device.get_info.router, prefix="/api", tags=["core"])
app.include_router(device.get_hostname.router, prefix="/api", tags=["core"])
app.include_router(device.get_time.router, prefix="/api", tags=["core"])
app.include_router(device.get_interfaces.router, prefix="/api", tags=["core"])
app.include_router(device.get_system_resources.router, prefix="/api", tags=["core"])
app.include_router(device.get_interface_by_name.router, prefix="/api", tags=["core"])
app.include_router(device.set_timezone.router, prefix="/api", tags=["core"])
app.include_router(device.set_hostname.router, prefix="/api", tags=["core"])
app.include_router(device.set_ip_settings.router, prefix="/api", tags=["core"])
app.include_router(device.set_wifi.router, prefix="/api", tags=["core"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    
    Global HTTP exception handler.

    Args:
        request: The incoming request that caused the exception.
        exc: The HTTPException instance.

    Returns:
        JSONResponse: The error response with status code and detail.
    """
    # Log the exception details
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(DBAPIError)
async def sqlalchemy_exception_handler(request: Request, exc: DBAPIError):
    """
    Global exception handler for SQLAlchemy DBAPI exceptions.

    Args:
        request: The incoming request that caused the exception.
        exc: The DBAPIError instance.

    Returns:
        JSONResponse: The error response indicating a database error.
    """
    # Log the exception details
    logger.error(f"DBAPIError: {exc.detail}")
    return JSONResponse(
        status_code=400,
        content={"message": "An error occurred with the database."},
    )


# Run the application with Uvicorn if the script is executed directly
if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host=UVICORN_HOST, port=UVICORN_PORT, reload=True)
    except Exception as e:
        # Log any exception that occurs when trying to start the server
        logger.critical(f"Failed to start the server: {e}", exc_info=True)
