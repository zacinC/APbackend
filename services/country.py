

from sqlalchemy.orm import Session

from schemas import schemas
from database import models


def get_countries(db: Session):
    return db.query(models.Country).all()


def insert_country(country: schemas.CountryCreate, db: Session):
    to_insert = models.Country(country_name=country.country_name)

    db.add(to_insert)
    db.commit()
    db.refresh(to_insert)

    return to_insert
