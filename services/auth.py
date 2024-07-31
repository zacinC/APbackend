from typing import Optional
from sqlalchemy.orm import Session
from ..database import models
from ..schemas import schemas


def register(db: Session, user: schemas.UserCreate):
    fake = user.password
    db_user = models.User(name=user.name, lastname=user.lastname, phone_number=user.phone_number,
                          role_type=user.role_type, email=user.email, hashed_password=fake)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(db_user)
    return db_user


def login(db: Session):
    pass
