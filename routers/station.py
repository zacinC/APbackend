from typing import Annotated, List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status

from auth.deps import get_current_admin_user

from database.dbconfig import get_db
from services.station import get_stations, add_station, update_station, get_stations_filtered, delete_station_id, get_stations_count
from schemas import schemas

station_router = APIRouter()


@station_router.get("/stations/count", response_model=int, tags=["station"])
def get_all_stations_count(db: Session = Depends(get_db)):
    return get_stations_count(db=db)


@station_router.get("/stations/{page_number}", response_model=List[schemas.Station], tags=["station"])
def get_all_stations(page_number: int, db: Session = Depends(get_db)):
    return get_stations(page_number=page_number, db=db)


@station_router.get("/stations-filtered", response_model=List[schemas.Station], tags=["station"])
def get_all_stations_filtered(search: str, db: Session = Depends(get_db)):
    return get_stations_filtered(db, search)


@station_router.post("/stations", response_model=schemas.Station, tags=["station"])
def post_station(current_user: Annotated[schemas.User, Depends(get_current_admin_user)], station: schemas.StationCreate, db: Session = Depends(get_db)):
    return add_station(station, db)


@station_router.put("/stations/{id}", response_model=schemas.Station, tags=["station"], status_code=status.HTTP_201_CREATED)
def put_station(current_user: Annotated[schemas.User, Depends(get_current_admin_user)], id, station: schemas.StationCreate, db: Session = Depends(get_db)):
    return update_station(station, id, db)


@station_router.delete("/stations/{id}", tags=["station"])
def delete_station(current_user: Annotated[schemas.User, Depends(get_current_admin_user)], id: int, db: Session = Depends(get_db)):
    return delete_station_id(id, db)

