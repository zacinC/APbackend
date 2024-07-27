from typing import Optional
from sqlalchemy.orm import Session
from ..MySql import models
from ..schemas import schemas


def get_users(db: Session, page_number):
    return db.query(models.User).offset((page_number-1)*10).limit(10).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users_filtered(page_number: int, db: Session, username: Optional[str], full_name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None):
    if not email:
        email = ""
    if not name:
        name = ""
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
