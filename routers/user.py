
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter

from ..MySql.database import get_db
from ..services.user import get_users
from ..schemas import schemas

user_router = APIRouter()


@user_router.get("/users/", response_model=list[schemas.User],tags = ["user"])
def get_all_users(db: Session = Depends(get_db)):
    users = get_users(db)
    return users
