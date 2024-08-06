from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter

from auth.deps import get_current_admin_user
from database.dbconfig import get_db
from services.role import get_roles
from schemas import schemas

role_router = APIRouter()


@role_router.get("/roles/", response_model=list[schemas.Role], tags=["role"])
def get_all_roles(current_user: Annotated[schemas.User, Depends(get_current_admin_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_roles(db, skip=skip, limit=limit)
    return users
