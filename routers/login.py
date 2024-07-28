from ..settings import ACCESS_TOKEN_EXPIRE_MINUTES
from ..MySql import models
from ..MySql.database import SessionLocal, get_db
from ..schemas.schemas import UserBase, Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from ..auth.security import authenticate_user, create_access_token
from ..auth.deps import get_current_active_user, get_current_user
from fastapi import Depends, APIRouter, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session

login_router = APIRouter()


@login_router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends(
        )], db: Session = Depends(get_db)):
    user = await authenticate_user(
        form_data.username, form_data.password, db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
