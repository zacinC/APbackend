from typing import List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi import APIRouter,status

from ..MySql.database import get_db
from ..services.auth import register
from ..services.user import get_user_by_email

from ..schemas import schemas

auth_router = APIRouter()

@auth_router.post("/register",response_model=schemas.User,tags = ["auth"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
  
    return register(db=db, user=user)