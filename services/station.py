

from sqlalchemy.orm import Session
from ..MySql import models
from ..schemas import schemas




def get_stations(db:Session):
    return db.query(models.Station).all()

def add_station(station:schemas.StationCreate,db:Session):
    station_to_add = models.Station(station)

    db.add(station_to_add)
    db.commit()
    db.refresh(station_to_add)
    return station_to_add
