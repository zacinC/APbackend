from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from services.user import get_user_by_email, get_user_by_username
from schemas.schemas import TokenData, User, UserBase
from database.dbconfig import SessionLocal, get_db
from settings import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Svudje stoji username jer auth koji fastapi koristi u pozadini prihvata samo
# username kao pozicioni argument i varijabla se uvjek mora tako zvati
async def get_user(username: str, db: Session):
    user = get_user_by_username(db, username)
    if user is None:
        user = get_user_by_email(db, username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    if current_user.role_type != 'Admin':
        raise HTTPException(
            status_code=403, detail="User doesn't have Admin privileges!")
    return current_user


async def get_current_driver_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    if current_user.role_type != 'Driver':
        raise HTTPException(
            status_code=403, detail="User is not a driver!")
    return current_user
