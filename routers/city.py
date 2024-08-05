from typing import Annotated, List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status

from auth.deps import get_current_admin_user

from database.dbconfig import get_db
from services.city import get_cities, insert_city
from schemas import schemas

city_router = APIRouter()

# napraviti post za gradove


@city_router.get("/cities", response_model=List[schemas.CityCreate], tags=["city"])
def get_all_cities(city_name: Optional[str] = None, db: Session = Depends(get_db)):
    return get_cities(db=db, city_name=city_name)


@city_router.post("/cities", response_model=schemas.City, tags=["city"])
def post_city(current_user: Annotated[schemas.User, Depends(get_current_admin_user)], city: schemas.CityCreate, db: Session = Depends(get_db)):
    return insert_city(city, db)
