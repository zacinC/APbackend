from typing import List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status

from ..database.dbconfig import get_db
from ..services.route import get_routes, get_routes_filtered, delete_routeID, create_route, get_routes_filtered_by_company, update, activate_deactivate
from ..schemas import schemas
from datetime import datetime

route_router = APIRouter()


@route_router.get("/routes", response_model=List[schemas.RouteResponse], tags=["route"])
def get_all_routes(companyname: Optional[str] = None, db: Session = Depends(get_db)):
    if companyname:
        return get_routes_filtered_by_company(db, companyname)
    return get_routes(db)


@route_router.get("/routes/{startCity}-{startCountry}/{endCity}-{endCountry}/{date}", response_model=List[schemas.RouteResponse], tags=["route"])
def get_filtered_routes(
        startCity: str,
        startCountry: str,
        endCity: str,
        endCountry: str,
        date: Optional[datetime],
        db: Session = Depends(get_db)):

    all_routes_filtered = get_routes_filtered(
        db, startCity, startCountry, endCity, endCountry, date)
    return all_routes_filtered


@route_router.delete("/routes/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["route"])
def delete_route(id: int, day_name: Optional[str] = None, db: Session = Depends(get_db)):

    return delete_routeID(db, id, day_name)


@route_router.post("/routes", response_model=schemas.Route, status_code=status.HTTP_201_CREATED, tags=["route"])
def post_route(info: schemas.RouteCreateRequest, db: Session = Depends(get_db)):
    return create_route(info.days, info.stations, info.company_id, db)


@route_router.put("/routes/{id}", response_model=schemas.Route, status_code=status.HTTP_201_CREATED, tags=["route"])
def update_route(id, info: schemas.RouteCreateRequest, db: Session = Depends(get_db)):
    return update(id, info.days, info.stations, info.company_id, db)


@route_router.put("/routes/activate/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["route"])
def activate_deactivate_route(id, should_be_activated: bool, db: Session = Depends(get_db)):
    return activate_deactivate(id=id, should_be_activated=should_be_activated, db=db)
