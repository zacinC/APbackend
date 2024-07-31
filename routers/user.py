
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter

from ..database.dbconfig import get_db
from ..services.user import get_users, get_user_by_email, get_users_filtered, get_user_by_username, delete_user_by_id, update_role_by_id
from ..schemas import schemas

user_router = APIRouter()


# @user_router.get("/users/{username}", response_model=schemas.UserCreate, tags=["user"])
# def get_by_username(username: str, db: Session = Depends(get_db)):
#     user = get_user_by_username(db, username)

#     if user:
#         return user

#     raise HTTPException(status_code=404, detail="User not found!")


@user_router.get("/users/{page_number}", response_model=list[schemas.User], tags=["user"])
def get_all_users(page_number: int, username: Optional[str] = None, full_name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None, db: Session = Depends(get_db)):
    users = []

    if (email or username or full_name or role):
        users = get_users_filtered(
            page_number, db, username=username, full_name=full_name, email=email, role=role)
    else:
        users = get_users(db, page_number)
    return users


@user_router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["user"])
def delete_user(id: str, db: Session = Depends(get_db)):
    return delete_user_by_id(id=id, db=db)


@user_router.put("/users/{id}", response_model=schemas.User, tags=["user"])
def update_role(id: int, role_type: str, db: Session = Depends(get_db)):
    return update_role_by_id(id=id, role_type=role_type, db=db)
