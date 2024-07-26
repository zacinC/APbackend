from typing import List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter,status

from ..MySql.database import get_db
from ..services.country import get_countries
from ..schemas import schemas

country_router = APIRouter()

@country_router.get("/countries",response_model=List[schemas.CountryCreate],tags = ["country"])
def get_all_countries(db:Session = Depends(get_db)):
    return get_countries(db)

