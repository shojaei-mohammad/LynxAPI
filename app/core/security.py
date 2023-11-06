"""
Security Utilities Module

This module provides utility functions to handle authentication and token generation for the application.
It offers methods to verify hashed passwords, generate password hashes, create JWT access tokens,
and authenticate users against the database.

Main functionalities include:
- Password hashing and verification using bcrypt.
- JWT token creation with expiration.
- Authenticating users against the database.

Dependencies:
- jwt: For creating and decoding JWT tokens.
- passlib: For password hashing and verification.
- app.core.config: For application configurations like the secret key.
"""

from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import API_SECRET_KEY, API_ALGORITHM
from app.db.models import User
from app.utils.logger import configure_logger

# Setup logging
logger = configure_logger()


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Define the JWTError exception
class JWTError(Exception):
    """Custom exception for JWT-related errors."""

    pass


def decode_token(token: str):
    """
    Decode a JWT token and return the payload.

    Args:
    - token (str): The JWT token to decode.

    Returns:
    - dict: Decoded payload of the JWT token.

    Raises:
    - JWTError: If the token has expired or is invalid.
    """
    try:
        payload = jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise JWTError("Token has expired")
    except JWTError as e:
        logger.error(f"Invalid token. Reason: {str(e)}")
        raise JWTError("Invalid token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hashed version.

    Args:
    - plain_password (str): The plain-text password to verify.
    - hashed_password (str): The hashed version of the password.

    Returns:
    - bool: True if the password matches the hash, False otherwise.
    """
    return password_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.

    Args:
    - data (dict): The data payload to include in the token.
    - expires_delta (timedelta, optional): The duration the token should remain valid for.

    Returns:
    - str: The JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm="HS256")
    except Exception as e:
        logger.error(f"Error encoding JWT: {e}")
        raise ValueError("Error encoding JWT")
    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str) -> bool:
    """
    Authenticate a user against the users stored in the database.

    Args:
    - db (Session): The database session to use for queries.
    - username (str): The username to authenticate.
    - password (str): The associated password.

    Returns:
    - bool: True if authentication was successful, False otherwise.
    """
    try:
        # Fetch the user from the database
        user = db.query(User).filter(User.username == username).first()

        # If the user exists and the password is correct, return True
        if user and verify_password(password, user.hashed_password):
            return True
        return False
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        return False


__all__ = [
    "decode_token",
    "verify_password",
    "create_access_token",
    "authenticate_user",
]
