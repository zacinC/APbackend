from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..auth.utils import get_password_hash
from ..database import models
from ..schemas import schemas
from ..auth import utils


def get_users(db: Session, page_number):
    return db.query(models.User).offset((page_number-1)*10).limit(10).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users_filtered(page_number: int, db: Session, username: Optional[str] = None, full_name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None):
    if not email:
        email = ""
    if not username:
        username = ""
    if not full_name:
        full_name = ""
    if not role:
        role = ""

    print(email)

    return db.query(models.User).filter(models.User.email.like(f'%{email}%'),
                                        models.User.username.like(
                                            f'%{username}%'),
                                        models.User.full_name.like(
                                            f'%{full_name}%'),
                                        models.User.role_type.like(f'%{role}')).offset((page_number-1)*10).limit(10).all()


def create_user(db: Session, user_create: schemas.UserRegister | schemas.UserCreate) -> models.User:
    db_obj = models.User(
        email=user_create.email,
        username=user_create.username,
        full_name=user_create.full_name,
        phone_number=user_create.phone_number,
        hashed_password=get_password_hash(user_create.password),
        role_type=user_create.role_type
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_user_by_id(id: int, db: Session):

    user_to_delete = db.query(models.User).filter(models.User.id == id).first()

    if not user_to_delete:
        raise HTTPException(
            status_code=404, detail=f'User with {id} not found!')

    db.delete(user_to_delete)

    db.commit()

# Ovo treba da bude update user

def update_single_user(id: int, update:schemas.UserRegister, db: Session) -> models.User:

    user_to_update = db.query(models.User).filter(models.User.id == id).first()
    if not user_to_update:
        raise HTTPException(
            status_code=404, detail=f'User with {id} not found!')
    
    if update.role_type:
        user_to_update.role_type = update.role_type
    if update.email != user_to_update.email:
        user_to_update.email = update.email
    if update.full_name != user_to_update.full_name:
        user_to_update.full_name = update.full_name
    if update.password:
        user_to_update.hashed_password = utils.get_password_hash(update.password)
    if update.username != user_to_update.username:
        user_to_update.username = update.username
    if update.phone_number:
        user_to_update.phone_number = update.phone_number
    if update.company_id:
        user_to_update.company_id = update.company_id
    

    db.commit()

    db.refresh(user_to_update)

    return user_to_update
