from typing import Optional
from sqlalchemy.orm import Session
from ..MySql import models
from ..schemas import schemas


def get_users(db: Session,page_number):
    return db.query(models.User).offset((page_number-1)*10).limit(10).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users_filtered(page_number:int,db:Session,name:Optional[str] = None,lastname:Optional[str] = None,email:Optional[str] = None,role:Optional[str] = None):
    if not email:
        email = ""
    if not name:
        name = ""
    if not lastname:
        lastname = ""
    if not role:
        role = ""
    
    print(email)

    return db.query(models.User).filter(models.User.email.like(f'%{email}%'),
                                        models.User.name.like(f'%{name}%'),
                                        models.User.lastname.like(f'%{lastname}%'),
                                        models.User.role_type.like(f'%{role}')).offset((page_number-1)*10).limit(10).all()
