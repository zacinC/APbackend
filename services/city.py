from typing import Optional
from sqlalchemy.orm import Session
from ..database import models


def get_cities(db: Session,city_name:Optional[str] = None):
    if not city_name:
        city_name = ""
    return db.query(models.City).filter(models.City.city_name.like(f'%{city_name}%')).all()