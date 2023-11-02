from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.admin.authorization import oauth2_scheme
from app.core.security import decode_token, JWTError
from app.db.database import get_db
from app.db.models import User


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token_data = Token(username=username)

    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise credentials_exception
    return user
