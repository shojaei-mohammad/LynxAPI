"""
Token Authorization Module

This module handles the token-based authentication for the application.
It provides an endpoint for clients to obtain access tokens using the OAuth2 password flow.
Clients, usually frontends, can provide a username and password, and if authenticated successfully,
receive an access token in return. This token can then be used to access other protected endpoints.

The main function in this module is `login_for_access_token`, which performs the actual authentication
and token generation. It makes use of utility functions and settings from other modules to validate
user credentials and generate JWT tokens.
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security import authenticate_user, create_access_token
from app.schemas.token import Token
from app.core import config
from app.utils.logger import configure_logger

logger = configure_logger()

router = APIRouter()

# Using OAuth2 password flow, where the client (usually a frontend) will collect the username and password,
# then send them to the server to get an access token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/token")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate the user.

    Given the username and password in the form data, this function will authenticate the user,
    and if successful, return an access token. The token can then be used to access protected routes.

    Args:
    - form_data (OAuth2PasswordRequestForm): A form with fields `username` and `password`.

    Returns:
    - dict: A dictionary containing the access token and token type ("bearer").

    Raises:
    - HTTPException: If authentication fails.
    """
    # Authenticate the user with the provided username and password.

    if not authenticate_user(form_data.username, form_data.password):
        logger.warning("Incorrect username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Set the expiration time for the access token.
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Create the access token with the specified expiration time.
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
