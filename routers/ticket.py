from typing import List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter,status

from ..MySql.database import get_db
from ..services.ticket import get_tickets_one_user
from ..schemas import schemas

ticket_router = APIRouter()


@ticket_router.get("/station",response_model=List[schemas.StationCreate],tags=["tickets"])
def get_all_tickets_one_user(db:Session = Depends(get_db)):
    return get_tickets_one_user(db)


