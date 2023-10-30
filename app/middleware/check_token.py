"""
JWT Token Middleware for FastAPI.

This middleware intercepts incoming requests to validate the presence and correctness
of a JWT token provided in the Authorization header. Valid tokens allow the request
to proceed, while invalid or missing tokens return a 401 Unauthorized response.

The middleware excludes certain routes from token checking, such as documentation routes
and the token generation endpoint.
"""

from fastapi import Request, status
from starlette.types import ASGIApp, Scope, Receive, Send
import jwt
from app.core.security import SECRET_KEY
from app.utils.logger import configure_logger
from starlette.responses import JSONResponse

logger = configure_logger()

class JWTTokenMiddleware:
    """
    Middleware to check for valid JWT tokens in incoming requests.

    Attributes:
    - app: The ASGI application instance to forward requests to.

    Methods:
    - __call__: The method to intercept requests and check for valid tokens.
    """

    def __init__(self, app: ASGIApp):
        """
        Initialize the JWTTokenMiddleware.

        Args:
        - app: The ASGI application instance to forward requests to.
        """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """
        Intercept incoming requests to check for valid JWT tokens.

        Args:
        - scope: The ASGI scope for the current request.
        - receive: The ASGI receive callable.
        - send: The ASGI send callable.
        """
        request = Request(scope, receive=receive)

        # Check if the request path is in the list of excluded routes.
        # If so, forward the request without token checking.
        if request.url.path in [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/admin/token",
        ]:
            await self.app(scope, receive, send)
            return

        # Extract the token from the Authorization header.
        token = request.headers.get("Authorization")

        # If no token is found, log the unauthorized access attempt and send a custom response.
        if not token:
            logger.warning(
                f"Unauthorized access attempt detected from IP {request.client.host}"
            )
            response = JSONResponse(
                content={"detail": "Token is missing"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            await response(scope, receive, send)
            return

        # Try to decode the token using the SECRET_KEY.
        # If decoding fails, log the error and send a custom response.
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.state.user = payload.get("sub")
        except jwt.PyJWTError as e:
            logger.error(f"Token validation error: {e}")
            response = JSONResponse(
                content={"detail": "Token is invalid"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            await response(scope, receive, send)
            return

        # If the token is valid, forward the request.
        await self.app(scope, receive, send)
