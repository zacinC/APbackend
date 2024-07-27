
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi import APIRouter

from ..MySql.database import get_db
from ..services.user import get_users, get_user_by_email, get_users_filtered, get_user_by_username
from ..schemas import schemas

user_router = APIRouter()


@user_router.get("/users/{username}", response_model=schemas.UserCreate, tags=["user"])
def get_by_username(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)

    if user:
        return user

    raise HTTPException(status_code=404, detail="User not found!")


@user_router.get("/users/{page_number}", response_model=list[schemas.User], tags=["user"])
def get_all_users(page_number: int, username: Optional[str], fullname: Optional[str], email: Optional[str] = None, name: Optional[str] = None, lastname: Optional[str] = None, role: Optional[str] = None, db: Session = Depends(get_db)):
    users = []

    print(email, name, lastname)

    if (email or name or lastname or role):
        users = get_users_filtered(
            page_number, db, name=name, lastname=lastname, email=email, role=role)
    else:
        users = get_users(db, page_number)
    return users
