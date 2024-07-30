

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..MySql import models
from ..schemas import schemas




def get_stations(db:Session):
    return db.query(models.Station).all()

def get_stations_filtered(db: Session, search: str):
    return db.query(models.Station).filter(
        or_(
            models.Station.address.like(f'%{search}%'),
            models.Station.city_name.like(f'%{search}%'),
            models.Station.country_name.like(f'%{search}%')
        )
    ).all()
def add_station(station:schemas.StationCreate,db:Session):
    station_to_add = models.Station(city_name = station.city_name,country_name = station.country_name,phone_number = station.phone_number,address = station.address)

    db.add(station_to_add)
    db.commit()
    db.refresh(station_to_add)
    return station_to_add

def update_station(station:schemas.Station,id:int,db:Session):
    
    db_station = db.query(models.Station).filter(models.Station.id == id).first()

    if not db_station:
        raise HTTPException(status_code = 404,detail = "Station not found!")
    
    for key, value in vars(station).items():
        setattr(db_station, key, value)
        
    db.commit()
    db.refresh(db_station)

    return db_station

def delete_station_id(id: int, db: Session):
    db_station = db.query(models.Station).filter(models.Station.id == id).first()

    if not db_station:
        raise HTTPException(status_code=404, detail="Station not found!")

    db.delete(db_station)
    db.commit()

    return {"detail": "Station deleted successfully"}

    
