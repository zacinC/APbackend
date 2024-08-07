from math import ceil
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from auth.utils import get_password_hash
from database import models
from schemas import schemas
from auth import utils


def get_users(db: Session, page_number):
    all_users = db.query(models.User,models.Company.company_name).outerjoin(models.Company)\
                                        .offset((page_number-1)*10).limit(10).all()
    list_to_return = []
    for user in all_users:
        temp_user = user[0]
        temp_user.company_name = user[1]
        list_to_return.append(temp_user)
    
    return list_to_return

def get_count_users(db: Session):
    return ceil(len(db.query(models.User).all()) / 10)


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if user and user.company_id:
        user_with_company_name = db.query(models.User,models.Company).filter(models.Company.id == user.company_id). \
        filter(models.User.email == email).first()
        user.company_name = user_with_company_name[1]

    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()

    if user and user.company_id:
        user_with_company_name = db.query(models.User, models.Company.company_name). \
            join(models.Company, models.Company.id == user.company_id). \
            filter(models.User.username == username).first()
        user.company_name = user_with_company_name[1]

    return user


def get_count_users_filtered(db: Session, username: Optional[str] = None, full_name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None):
    if not email:
        email = ""
    if not username:
        username = ""
    if not full_name:
        full_name = ""
    if not role:
        role = ""

    return ceil(len(db.query(models.User).filter(models.User.email.like(f'%{email}%'),
                                                 models.User.username.like(
        f'%{username}%'),
        models.User.full_name.like(
        f'%{full_name}%'),
        models.User.role_type.like(f'%{role}%')).all()) / 10)


def get_users_filtered(page_number: int, db: Session, username: Optional[str] = None, full_name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None):
    if not email:
        email = ""
    if not username:
        username = ""
    if not full_name:
        full_name = ""
    if not role:
        role = ""

    list_to_return = []

    all_users = db.query(models.User,models.Company.company_name).outerjoin(models.Company).filter(models.User.email.like(f'%{email}%'),
                                        models.User.username.like(
                                            f'%{username}%'),
                                        models.User.full_name.like(
                                            f'%{full_name}%'),
                                        models.User.role_type.like(f'%{role}')).offset((page_number-1)*10).limit(10).all()
    
    for user in all_users:
        temp_user = user[0]
        temp_user.company_name = user[1]
        list_to_return.append(temp_user)

    return list_to_return    

def create_user(db: Session, user_create: schemas.UserRegister | schemas.UserCreate) -> models.User:
    db_obj = models.User(
        email=user_create.email,
        username=user_create.username,
        full_name=user_create.full_name,
        phone_number=user_create.phone_number,
        hashed_password=get_password_hash(user_create.password),
        role_type=user_create.role_type,
        company_id=user_create.company_id
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
    
    all_tickets_user = db.query(models.Ticket).filter(models.Ticket.passenger_id == id)

    for ticket in all_tickets_user:
        db.delete(ticket)
    
    db.commit()
    db.delete(user_to_delete)

    db.commit()

# Ovo treba da bude update user


def update_single_user(id: int, updated_user: schemas.UserUpdate, db: Session) -> models.User:

    user_to_update = db.query(models.User).filter(models.User.id == id).first()
    if not user_to_update:
        raise HTTPException(
            status_code=404, detail=f'User with {id} not found!')

    if updated_user.role_type:
        user_to_update.role_type = updated_user.role_type
    if updated_user.email and updated_user.email != user_to_update.email:
        user_to_update.email = updated_user.email
    if updated_user.full_name and updated_user.full_name != user_to_update.full_name:
        user_to_update.full_name = updated_user.full_name
    if updated_user.password:
        user_to_update.hashed_password = utils.get_password_hash(
            updated_user.password)
    if updated_user.username and updated_user.username != user_to_update.username:
        user_to_update.username = updated_user.username
    if updated_user.phone_number:
        user_to_update.phone_number = updated_user.phone_number
    if updated_user.company_id:
        user_to_update.company_id = updated_user.company_id
    if updated_user.disabled and updated_user.disabled != user_to_update.disabled:
        user_to_update.disabled = updated_user.disabled

    db.commit()

    db.refresh(user_to_update)

    return user_to_update
