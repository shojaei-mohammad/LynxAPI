"""
Security Utilities Module

This module provides utility functions to handle authentication and token generation for the application.
It offers methods to verify hashed passwords, generate password hashes, create JWT access tokens,
and authenticate users against the system's user accounts using the PAM (Pluggable Authentication Modules) interface.

Main functionalities include:
- Password hashing and verification using bcrypt.
- JWT token creation with expiration.
- Authenticating users against the system using PAM.

Note: This module assumes the system is UNIX-like with PAM support.

Dependencies:
- jwt: For creating and decoding JWT tokens.
- pam: For UNIX system user authentication.
- passlib: For password hashing and verification.
- app.core.config: For application configurations like the secret key.
"""

import jwt
from datetime import datetime, timedelta
import pam
from passlib.context import CryptContext
from app.core import config
from app.utils.logger import configure_logger

# Setup logging
logger = configure_logger()

# Secret key to encode and decode JWT token
SECRET_KEY = config.SECRET_KEY

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def get_password_hash(password: str) -> str:
    """
    Generate a bcrypt hashed version of the password.

    Args:
    - password (str): The plain-text password to hash.

    Returns:
    - str: The hashed version of the password.
    """
    return password_context.hash(password)


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
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    except Exception as e:
        logger.error(f"Error encoding JWT: {e}")
        raise ValueError("Error encoding JWT")
    return encoded_jwt


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user against the system's user accounts.

    Args:
    - username (str): The username to authenticate.
    - password (str): The associated password.

    Returns:
    - bool: True if authentication was successful, False otherwise.
    """
    p = pam.pam()
    try:
        return p.authenticate(username, password)
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        return False
