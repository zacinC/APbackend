from typing import Optional
from sqlalchemy.orm import Session
from database import models
from schemas import schemas


def get_cities(db: Session, city_name: Optional[str] = None):
    if not city_name:
        city_name = ""
    return db.query(models.City).filter(models.City.city_name.like(f'%{city_name}%')).all()


def insert_city(city: schemas.CityCreate, db: Session):
    to_insert = models.City(
        country_name=city.country_name, city_name=city.city_name)

    db.add(to_insert)
    db.commit()
    db.refresh(to_insert)

    return to_insert
