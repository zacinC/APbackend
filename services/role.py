from sqlalchemy.orm import Session
from ..MySql import models


def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()
