
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi import APIRouter

from ..MySql.database import get_db
from ..services.user import get_users,get_user_by_email,create_user,get_users_filtered
from ..schemas import schemas

user_router = APIRouter()


@user_router.get("/users/{page_number}", response_model=list[schemas.User],tags = ["user"])
def get_all_users(page_number:int,email:Optional[str] = None,name:Optional[str] = None,lastname:Optional[str] = None,role:Optional[str] = None,db: Session = Depends(get_db)):
    users = []

    print(email,name,lastname)

    if(email or name or lastname or role):
        users = get_users_filtered(page_number,db,name = name,lastname = lastname,email = email,role = role)
    else:
        users = get_users(db,page_number)
    return users


@user_router.post("/users/", response_model=schemas.User,tags = ["user"])
def post_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(user.email)
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print(user)
    return create_user(db=db, user=user)

