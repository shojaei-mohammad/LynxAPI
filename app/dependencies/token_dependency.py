# app/dependencies/token_dependency.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.security import SECRET_KEY

# Use OAuth2PasswordBearer for token extraction
security = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/token")


async def get_current_user(token: str = Depends(security)):
    """
    Decode the token using JWT and return the current user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
