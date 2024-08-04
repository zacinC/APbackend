from typing import List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status

from ..database.dbconfig import get_db
from ..services.country import get_countries, insert_country
from ..schemas import schemas

country_router = APIRouter()

# post za drzave

@country_router.get("/countries", response_model=List[schemas.CountryCreate], tags=["country"])
def get_all_countries(db: Session = Depends(get_db)):
    return get_countries(db)

@country_router.post("/cities", response_model=List[schemas.CityCreate], tags=["city"])
def post_country(country:schemas.CountryCreate,db:Session = Depends(get_db)):
    return insert_country(country,db)
