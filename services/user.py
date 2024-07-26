from typing import Optional
from sqlalchemy.orm import Session
from ..MySql import models
from ..schemas import schemas


def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users_filtered(db:Session,name:Optional[str] = None,lastname:Optional[str] = None,email:Optional[str] = None):
    if not email:
        email = ""
    if not name:
        name = ""
    if not lastname:
        lastname = ""
    
    print(email)

    return db.query(models.User).filter(models.User.email.like(f'%{email}%'),models.User.name.like(f'%{name}%'),models.User.lastname.like(f'%{lastname}%'))

def create_user(db: Session, user: schemas.UserCreate):
    fake= user.password # ovdje ide logika za hesovanje passworda
    db_user = models.User(name = user.name,lastname = user.lastname,phone_number = user.phone_number,role_type = user.role_type,email=user.email, hashed_password=fake)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(db_user)
    return db_user
