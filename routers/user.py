
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter

from ..MySql.database import get_db
from ..services.user import get_users
from ..schemas import schemas

user_router = APIRouter()


@user_router.get("/users/", response_model=list[schemas.User],tags = ["user"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users
