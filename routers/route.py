from typing import Annotated, List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status

from auth.deps import get_current_admin_user, get_current_driver_user

from database.dbconfig import get_db
from services.route import get_routes, get_routes_filtered, delete_routeID, create_route, get_routes_filtered_by_company, update, activate_deactivate, get_route_by_id,get_routes_filtered_by_company_id
from schemas import schemas
from datetime import datetime

route_router = APIRouter()

@route_router.get("/routes_paginated/count",response_model=int, tags=["route"])
def get_all_routes(companyname: Optional[str] = None, company_id:Optional[int] = None,db: Session = Depends(get_db),is_active:Optional[int] = None):
    if companyname:
        return get_routes_filtered_by_company(True,-1,db, companyname,is_active)
    if company_id:
        return get_routes_filtered_by_company_id(True,-1,db,company_id,is_active)
    
    return get_routes(True,-1,db,is_active)


@route_router.get("/routes_filtered/count",response_model = int,tags=["route"])
def get_filtered_routes(
        startCity: Optional[str] = None,
        startCountry: Optional[str] = None,
        endCity: Optional[str] = None,  
        endCountry: Optional[str] = None,
        date: Optional[datetime] = None,
        price_from:Optional[float] = None,
        price_to:Optional[float] = None,
        companyname:Optional[str] = None,
        db: Session = Depends(get_db)):
        

    all_routes_filtered = get_routes_filtered(True,-1,
        db, startCity, startCountry, endCity, endCountry, date,price_from,price_to,companyname)
    return all_routes_filtered



@route_router.get("/routes_paginated/{page_number}", response_model=List[schemas.RouteResponse], tags=["route"])
def get_all_routes(page_number:int,companyname: Optional[str] = None, company_id:Optional[int] = None,db: Session = Depends(get_db),is_active:Optional[int] = None):
    if companyname:
        return get_routes_filtered_by_company(False,page_number,db, companyname,is_active)
    
    if company_id:
        return get_routes_filtered_by_company_id(False,page_number,db,company_id,is_active)
    
    return get_routes(False,page_number,db,is_active)


@route_router.get("/routes_filtered/{page_number}", response_model=List[schemas.RouteResponse], tags=["route"])
def get_filtered_routes(
        page_number: int,
        startCity: Optional[str] = None,
        startCountry: Optional[str] = None,
        endCity: Optional[str] = None,
        endCountry: Optional[str] = None,
        date: Optional[datetime] = None,
        price_from:Optional[float] = None,
        price_to:Optional[float] = None,
        companyname:Optional[str] = None,
        db: Session = Depends(get_db)):
        
    all_routes_filtered = get_routes_filtered(False,page_number,
        db, startCity, startCountry, endCity, endCountry, date,price_from,price_to,companyname)
    return all_routes_filtered


@route_router.delete("/routes/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["route"])
def delete_route(current_user: Annotated[schemas.User, Depends(get_current_admin_user)],id: int, day_name: Optional[str] = None, db: Session = Depends(get_db)):

    return delete_routeID(db, id, day_name)


@route_router.get("/routes/{id}", response_model=List[schemas.RouteResponse], tags=["route"])
def get_single_route_by_id(id: int, db: Session = Depends(get_db)):
    return get_route_by_id(id, db)


@route_router.post("/routes", response_model=schemas.Route, status_code=status.HTTP_201_CREATED, tags=["route"])
def post_route(current_user: Annotated[schemas.User, Depends(get_current_driver_user)], info: schemas.RouteCreateRequest, db: Session = Depends(get_db)):
    return create_route(info.days, info.stations, current_user.company_id, db)


@route_router.put("/routes/{id}", response_model=schemas.Route, status_code=status.HTTP_201_CREATED, tags=["route"])
def update_route(current_user: Annotated[schemas.User, Depends(get_current_driver_user)], id, info: schemas.RouteCreateRequest, db: Session = Depends(get_db)):
    return update(id, info.days, info.stations, current_user.company_id, db)


@route_router.put("/routes/activate/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["route"])
def activate_deactivate_route(current_user: Annotated[schemas.User, Depends(get_current_admin_user)], id, should_be_activated: bool, db: Session = Depends(get_db)):
    return activate_deactivate(id=id, should_be_activated=should_be_activated, db=db)
