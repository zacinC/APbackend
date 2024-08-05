from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import Depends
import jwt
from .utils import verify_password
from settings import ALGORITHM, SECRET_KEY
from .deps import get_user
from database.dbconfig import get_db


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = await get_user(username, db)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user
