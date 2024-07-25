from sqlalchemy.orm import Session
from ..MySql import models



def get_cities(db:Session):
    return db.query(models.City).all()
    