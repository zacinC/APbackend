from fastapi.responses import HTMLResponse
from ..settings import ACCESS_TOKEN_EXPIRE_MINUTES
from ..MySql import models
from ..MySql.database import SessionLocal, get_db
from ..schemas.schemas import UserBase, Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from ..auth.security import authenticate_user, create_access_token
from ..auth.deps import get_current_active_user, get_current_user
from ..auth.utils import generate_password_reset_email, get_password_hash, send_email, verify_password_reset_token, generate_password_reset_token
from fastapi import Depends, APIRouter, Form, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session
from ..schemas.schemas import Message, NewPassword
from ..services.user import get_user_by_email, get_user_by_username


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


@login_router.get("/users/me", response_model=UserBase, tags="Test access token")
async def read_users_me(
    current_user: Annotated[UserBase, Depends(get_current_user)]
):
    return current_user


# @login_router.post("/reset-password", response_model=None)
# def reset_password(body: NewPassword, db: Session = Depends(get_db)):
#     email = verify_password_reset_token(token=body.token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     # Ovo treba da se sredi da moze da se uloguje preko mejla i preko usernamea, za sad ovo email je username
#     # user = get_user_by_email(db, email=email)
#     user = get_user_by_username(db, email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this email does not exist in the system.",
#         )
#     hashed_password = get_password_hash(password=body.new_password)
#     user.hashed_password = hashed_password
#     db.add(user)
#     db.commit()
#     return Message(message="Password updated successfully")


@login_router.post("/reset-password/")
def reset_password(
    token: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    email = verify_password_reset_token(token=token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    # Ovo treba da se sredi da moze da se uloguje preko mejla i preko usernamea, za sad ovo email je username
    # user = get_user_by_email(db, email=email)
    user = get_user_by_username(db, email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    hashed_password = get_password_hash(password=new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return Message(message="Password updated successfully")


@login_router.get("/recover-password/{token}", response_class=HTMLResponse)
async def password_recovery_form(token: str):
    return f"""
    <html>
        <head>
            <title>Reset Password</title>
        </head>
        <body>
            <h1>Reset Your Password</h1>
            <form action="/reset-password/" method="post">
                <input type="hidden" name="token" value="{token}">
                <label for="new_password">New Password:</label><br>
                <input type="password" id="new_password" name="new_password" required><br><br>
                <label for="confirm_password">Confirm New Password:</label><br>
                <input type="password" id="confirm_password" name="confirm_password" required><br><br>
                <button type="submit">Reset Password</button>
            </form>
        </body>
    </html>
    """


@login_router.post("/recover-password", response_model=Message)
async def recover_password(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )

    email_data = generate_password_reset_email(user)
    send_email(user, email_data["html_content"], email_data["subject"])

    return Message(message="Password recovery email sent")
