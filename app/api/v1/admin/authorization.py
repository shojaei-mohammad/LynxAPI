"""
Token Authorization Module

This module handles the token-based authentication for the application. It provides an endpoint for clients
to obtain access tokens using the OAuth2 password flow. Clients can provide a username and password to
receive an access token in return. This token can then be used to access other protected endpoints.
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import config
from app.core.security import authenticate_user, create_access_token
from app.db.database import get_db
from app.schemas.token import Token
from app.utils.logger import configure_logger

# Setup logging
logger = configure_logger()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/token")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
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
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning("Incorrect username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": form_data.username,
    }
