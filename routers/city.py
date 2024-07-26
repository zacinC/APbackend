from typing import List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter,status

from ..MySql.database import get_db
from ..services.city import get_cities
from ..schemas import schemas

city_router = APIRouter()

@city_router.get("/cities",response_model=List[schemas.CityCreate],tags = ["city"])
def get_all_cities(db:Session = Depends(get_db)):
    return get_cities(db)
