

from sqlalchemy.orm import Session
from ..database import models


def get_countries(db: Session):
    return db.query(models.Country).all()
