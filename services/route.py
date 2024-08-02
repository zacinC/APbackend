from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..database import models
import datetime


def get_routes(page_number,db: Session,is_active:Optional[bool] = None):
    routes_filtered = db.query(models.RouteDay.route_id, models.Company.company_name, models.RouteDay.day_name, models.RouteStationAssociation, models.Station)\
        .filter(models.Company.id == models.RouteDay.company_id,
                models.RouteStationAssociation.columns.get(
                    "route_id") == models.RouteDay.route_id,
                models.Station.id == models.RouteStationAssociation.columns.get(
                    "station_id")
                ).offset((page_number-1)*10).limit(10).all()

    grouped_results = {}

    
    all_active = get_all_active(db)
    all_inactive = get_all_inactive(db)


    for item in routes_filtered:
        route_id = item[0]

        if is_active and is_active == 1:
            if route_id not in all_active:
                continue
        
        if is_active and is_active == -1:
            if route_id not in all_inactive:
                continue

        if route_id not in grouped_results:
            grouped_results[route_id] = {
                "company_name": item[1],
                "stations": [],
                "route_id":item[0]
            }

        grouped_results[route_id]["stations"].append({"station": item[9],
                                                      "arrival_time": item[7],
                                                      "departure_time": item[6],
                                                      "price":item[8]
                                                      })

    final_list = []

    for key, value in grouped_results.items():
        final_list.append(value)

 

    return final_list


def get_routes_filtered_by_company(page_number:int,db: Session, companyname: str,is_active:Optional[int] = None):
    routes_filtered = db.query(models.RouteDay.route_id, models.Company.company_name, models.RouteDay.day_name, models.RouteStationAssociation, models.Station)\
        .filter(models.Company.id == models.RouteDay.company_id, models.Company.company_name == companyname,
                models.RouteStationAssociation.columns.get(
                    "route_id") == models.RouteDay.route_id,
                models.Station.id == models.RouteStationAssociation.columns.get(
                    "station_id")
                ).offset((page_number-1)*10).limit(10).all()

    grouped_results = {}

    all_active = get_all_active(db)
    all_inactive = get_all_inactive(db)

    print("aaaaaaaaaa",routes_filtered)



    for item in routes_filtered:
        route_id = item[0]

        if is_active and is_active == 1:
            if route_id not in all_active:
                continue
        
        if is_active and is_active == -1:
            if route_id not in all_inactive:
                continue

        if route_id not in grouped_results:
            grouped_results[route_id] = {
                "company_name": item[1],
                "stations": [],
                "route_id":item[0]
            }

        grouped_results[route_id]["stations"].append({"station": item[9],
                                                      "arrival_time": item[7],
                                                      "departure_time": item[6],
                                                      "price":item[8]

                                                      })

    final_list = []

    for key, value in grouped_results.items():
        final_list.append(value)

    print(final_list)

    return final_list


def get_routes_filtered(page_number:int,db: Session, startCity: str, startCountry: str, endCity: str, endCountry: str, date: Optional[datetime.datetime],price_from:Optional[float] = None,price_to:Optional[float] = None):
    day_of_week_full = None
    if date:
        day_of_week_full = date.strftime('%A')
    else:
        day_of_week_full = datetime.datetime.now().strftime('%A')

    if not price_from:
        price_from = -1
    if not price_to:
        price_to = 10000
    
    if not startCity:
        startCity = ""
    if not startCountry:
        startCountry = ""
    if not endCity:
        endCity = ""
    if not endCountry:
        endCountry = ""
    

    startStations: List[models.Station] = db.query(models.Station).filter(
        models.Station.city_name.like(f'%{startCity}%'),
        models.Station.country_name.like(f'%{startCountry}%')
    ).all()

    endStations: List[models.Station] = db.query(models.Station).filter(
        models.Station.city_name.like(f'%{endCity}%'),
        models.Station.country_name.like(f'%{endCountry}%')
    ).all()

    startStations = [station.id for station in startStations]
    endStations = [station.id for station in endStations]

    print(startStations, endStations, day_of_week_full,price_from,price_to)


    routes: List[models.Route] = db.query(models.Route).filter(models.Route.departure_station_id.in_(
        startStations)).filter(models.Route.arrival_station_id.in_(endStations),
                               models.Route.price >= price_from,models.Route.price <= price_to).all()

    routesIds = [route.id for route in routes]


    routes_filtered: List = db.query(models.RouteDayAssociation, models.Company.company_name, models.RouteStationAssociation, models.Station).\
        filter(models.RouteDayAssociation.columns.get("route_id").in_(routesIds), models.Company.id == models.RouteDayAssociation.columns.get("company_id"),
               models.RouteDayAssociation.columns.get(
               'route_id') == models.RouteStationAssociation.columns.get('route_id'),
               models.RouteStationAssociation.columns.get(
               'station_id') == models.Station.id,
               models.RouteDayAssociation.columns.get('day_name') == day_of_week_full).order_by(models.RouteStationAssociation.columns.get('id'))  \
        .offset((page_number-1)*10).limit(10).all()
    grouped_results = {}

    print("aaaaaaaaaa",routes_filtered)


    for item in routes_filtered:
        route_id = item[1]
        if route_id not in grouped_results:
            grouped_results[route_id] = {
                "company_name": item[3],
                "stations": [],
                "route_id":item[1]
            }

        grouped_results[route_id]["stations"].append({"station": item[10],
                                                      "arrival_time": item[8],
                                                      "departure_time": item[7],
                                                      "price":item[9]

                                                      })

    final_list = []

    for key, value in grouped_results.items():
        final_list.append(value)

    print(final_list)

    return final_list


def delete_routeID(db: Session, id: int, day_name: str):
    route = None
    if not day_name:
        route: models.Route = db.query(models.Route).filter(
            models.Route.id == id).first()

    else:
        route: models.Route = db.query(models.RouteDay).filter(
            models.RouteDay.route_id == id, models.RouteDay.day_name == models.Day.day_name).first()

    if not route:
        raise HTTPException(
            status_code=404, detail=f'Route with ID: {id} not found!')

    try:
        db.delete(route)
        db.commit()
        return {"detail": "Route deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


def create_route(days: List[models.Day], stations: List, company_id: int, db: Session):
    startStation = stations[0]
    endStation = stations[-1]
    route_price = endStation.price

    new_route = models.Route(departure_station_id=startStation.station_id, arrival_station_id=endStation.station_id,
                             arrival_time=endStation.arrival_time, departure_time=startStation.departure_time,price = route_price,is_active = False)

    db.add(new_route)
    db.commit()

    for day in days:
        route_day = models.RouteDay(
            day_name=day.day_name, route_id=new_route.id, company_id=company_id)
        db.add(route_day)

    for station in stations:
        route_station = models.RouteStation(
            route_id=new_route.id,
            station_id=station.station_id,
            departure_time=station.departure_time,
            arrival_time=station.arrival_time
        )
        db.add(route_station)

    db.commit()

    return new_route


def update(id: int, days: List[models.Day], stations: List, company_id: int, db: Session):
    delete_routeID(db, id, None)
    return create_route(days, stations, company_id, db)


def activate_deactivate(id: int, should_be_activated: bool, db: Session):
    if not should_be_activated:
        delete_routeID(db, id, None)

    else:
        route_to_update = db.query(models.Route).filter(
            models.Route.id == id).first()
        route_to_update.is_active = 1
        db.commit()
        db.refresh(route_to_update)

def get_all_inactive(db:Session):
    routes = db.query(models.Route.id).filter(models.Route.is_active == 0).all()
    return [route[0] for route in routes]

def get_all_active(db:Session):
    routes = db.query(models.Route.id).filter(models.Route.is_active == 1).all()
    return [route[0] for route in routes]

def get_route_by_id(id:int,db:Session):
    print("ID",id)
    routes_filtered = db.query(models.RouteDay.route_id, models.Company.company_name, models.RouteDay.day_name, models.RouteStationAssociation, models.Station)\
        .filter(models.Company.id == models.RouteDay.company_id,
                id == models.RouteDay.route_id,
                models.Station.id == models.RouteStationAssociation.columns.get(
                    "station_id")
                ).all()

    grouped_results = {}

    for item in routes_filtered:
        route_id = item[0]

        if route_id not in grouped_results:
            grouped_results[route_id] = {
                "company_name": item[1],
                "stations": [],
                "route_id":item[0]
            }

        grouped_results[route_id]["stations"].append({"station": item[9],
                                                      "arrival_time": item[7],
                                                      "departure_time": item[6],
                                                      "price":item[8]
                                                      })
    final_list = []

    for key, value in grouped_results.items():
        final_list.append(value)

    print(final_list)

    return final_list
