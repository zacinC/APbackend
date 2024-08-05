from typing import Annotated, List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status

from auth.deps import get_current_admin_user

from database.dbconfig import get_db
from services.country import get_countries, insert_country
from schemas import schemas

country_router = APIRouter()

# post za drzave


@country_router.get("/countries", response_model=List[schemas.CountryCreate], tags=["country"])
def get_all_countries(db: Session = Depends(get_db)):
    return get_countries(db)


@country_router.post("/countries", response_model=schemas.Country, tags=["country"])
def post_country(current_user: Annotated[schemas.User, Depends(get_current_admin_user)], country: schemas.CountryCreate, db: Session = Depends(get_db)):
    return insert_country(country, db)
