from typing import List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter,status

from ..MySql.database import get_db
from ..services.station import get_stations,add_station,update_station
from ..schemas import schemas

station_router = APIRouter()


@station_router.get("/stations",response_model=List[schemas.StationCreate],tags=["station"])
def get_all_stations(db:Session = Depends(get_db)):
    return get_stations(db)

@station_router.post("/stations",response_model = schemas.StationCreate,tags=["station"])
def post_station(station:schemas.StationCreate,db:Session = Depends(get_db)):
    return add_station(station,db)

@station_router.put("/stations/{id}",tags=["station"],status_code=status.HTTP_201_CREATED)
def put_station(id,station:schemas.StationCreate,db:Session = Depends(get_db)):
    return update_station(station,id,db)
