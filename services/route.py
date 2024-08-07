from math import ceil
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from database import models
import datetime

def find_station(stations, to_find):
    for station in stations:
        if station["station"].id == to_find.id:
            return True
    return False

def get_routes(return_count: bool, page_number, db: Session, is_active: Optional[bool] = None):

    routes_filtered = None

    if is_active is None:
        routes_filtered = db.query(models.RouteDay.route_id, models.Company.company_name, models.RouteDay.day_name, models.RouteStationAssociation, models.Station,models.Company.id)\
            .join(models.Route,models.Route.id == models.RouteDay.route_id).filter(models.Company.id == models.RouteDay.company_id,
                    models.RouteStationAssociation.columns.get(
                        "route_id") == models.RouteDay.route_id,
                    models.Station.id == models.RouteStationAssociation.columns.get(
                        "station_id"),
                    models.Route.parent_route == None,
                    ).order_by(models.RouteStationAssociation.columns.get(
                        "id")).all()
    else:
        routes_filtered = db.query(models.RouteDay.route_id, models.Company.company_name, models.RouteDay.day_name, models.RouteStationAssociation, models.Station,models.Company.id)\
        .join(models.Route,models.RouteDay.route_id == models.Route.id).filter(models.Company.id == models.RouteDay.company_id,
                models.RouteStationAssociation.columns.get(
                    "route_id") == models.RouteDay.route_id,
                models.Station.id == models.RouteStationAssociation.columns.get(
                    "station_id"),models.Route.is_active == is_active,models.Route.parent_route == None,

                ).order_by(models.RouteStationAssociation.columns.get(
                    "id")).all()

    grouped_results = {}
    seen_days = {}


    for item in routes_filtered:
        route_id = item[0]

        if route_id not in grouped_results:
            seen_days[route_id] = []
            grouped_results[route_id] = {
                "company_name": item[1],
                "stations": [],
                "days": [],
                "route_id": item[0],
                "company_id":item[10]

            }
        if not find_station(grouped_results[route_id]["stations"], item[9]):
            grouped_results[route_id]["stations"].append({"station": item[9],
                                                          "arrival_time": item[7],
                                                          "departure_time": item[6],
                                                          "price": item[8]
                                                          })
        if item[2] not in seen_days[route_id]:
            grouped_results[route_id]["days"].append({"day_name": item[2]})
            seen_days[route_id].append(item[2])

    final_list = []

    values_list = list(grouped_results.values())
    if return_count:
        return ceil(len(values_list) / 10)

    for i in range(0, 10):
        if ((page_number-1)*10 + i >= len(values_list)):
            break
        final_list.append(values_list[(page_number-1)*10 + i])

    return final_list

def get_routes_filtered_by_company_id(return_count:bool,page_number:int,db: Session, company_id: int,is_active:Optional[int] = None):
    routes_filtered = None


    if is_active is None:
        routes_filtered = db.query(models.RouteDay.route_id, models.Company.company_name, models.RouteDay.day_name, models.RouteStationAssociation, models.Station,models.Company.id)\
            .join(models.Route,models.Route.id == models.RouteDay.route_id).filter(models.Company.id == models.RouteDay.company_id, models.Company.id == company_id,
                    models.RouteStationAssociation.columns.get(
                        "route_id") == models.RouteDay.route_id,
                    models.Station.id == models.RouteStationAssociation.columns.get(
                        "station_id"),models.Route.parent_route == None,

                    ).order_by(models.RouteStationAssociation.columns.get(
                        "id")).all()
    else:
        routes_filtered = db.query(models.RouteDay.route_id, models.Company.company_name, models.RouteDay.day_name, models.RouteStationAssociation, models.Station,models.Company.id)\
        .join(models.Route,models.RouteDay.route_id == models.Route.id).filter(models.Company.id == models.RouteDay.company_id, models.Company.id == company_id,
                models.RouteStationAssociation.columns.get(
                    "route_id") == models.RouteDay.route_id,
                models.Station.id == models.RouteStationAssociation.columns.get(
                    "station_id"),models.Route.is_active == is_active,models.Route.parent_route == None,

                ).order_by(models.RouteStationAssociation.columns.get(
                    "id")).all()
            
    grouped_results = {}
    seen_days = {}

    
    for item in routes_filtered:
        route_id = item[0]


        if route_id not in grouped_results:
            seen_days[route_id] = []
            grouped_results[route_id] = {
                "company_name": item[1],
                "stations": [],
                "route_id":item[0],
                "days": [],
                "company_id":item[10]

            }
        if not find_station(grouped_results[route_id]["stations"],item[9]):
            grouped_results[route_id]["stations"].append({"station": item[9],
                                                        "arrival_time": item[7],
                                                        "departure_time": item[6],
                                                        "price":item[8]
                                                        })
        if item[2] not in seen_days[route_id]:
            grouped_results[route_id]["days"].append({"day_name": item[2]})
            seen_days[route_id].append(item[2])

    final_list = []

    values_list = list(grouped_results.values())

    if return_count:
        return ceil(len(values_list) / 10) 

    for i in range(0,10):
        if((page_number-1)*10 + i >= len(values_list)):
            break
        final_list.append(values_list[(page_number-1)*10 + i])
    
    return final_list


def get_routes_filtered_by_company(return_count: bool, page_number: int, db: Session, companyname: str, is_active: Optional[int] = None):

    routes_filtered = None

    if is_active is None:
        routes_filtered = db.query(models.RouteDay.route_id, models.Company.company_name, models.RouteDay.day_name, models.RouteStationAssociation, models.Station,models.Company.id)\
            .join(models.Route,models.Route.id == models.RouteDay.route_id).filter(models.Company.id == models.RouteDay.company_id, models.Company.company_name == companyname,
                    models.RouteStationAssociation.columns.get(
                        "route_id") == models.RouteDay.route_id,
                    models.Station.id == models.RouteStationAssociation.columns.get(
                        "station_id"),models.Route.parent_route == None,

                    ).order_by(models.RouteStationAssociation.columns.get(
                        "id")).all()
    else:
        routes_filtered = db.query(models.RouteDay.route_id, models.Company.company_name, models.RouteDay.day_name, models.RouteStationAssociation, models.Station,models.Company.id)\
        .join(models.Route,models.RouteDay.route_id == models.Route.id).filter(models.Company.id == models.RouteDay.company_id, models.Company.company_name == companyname,
                models.RouteStationAssociation.columns.get(
                    "route_id") == models.RouteDay.route_id,
                models.Station.id == models.RouteStationAssociation.columns.get(
                    "station_id"),models.Route.is_active == is_active,
                    models.Route.parent_route == None,
                ).order_by(models.RouteStationAssociation.columns.get(
                    "id")).all()
        
            
    grouped_results = {}
    seen_days = {}

    for item in routes_filtered:
        route_id = item[0]

        if route_id not in grouped_results:
            seen_days[route_id] = []
            grouped_results[route_id] = {
                "company_name": item[1],
                "stations": [],
                "route_id": item[0],
                "days": [],
                "company_id":item[10]
            }
        if not find_station(grouped_results[route_id]["stations"], item[9]):
            grouped_results[route_id]["stations"].append({"station": item[9],
                                                          "arrival_time": item[7],
                                                          "departure_time": item[6],
                                                          "price": item[8]
                                                          })
        if item[2] not in seen_days[route_id]:
            grouped_results[route_id]["days"].append({"day_name": item[2]})
            seen_days[route_id].append(item[2])

    final_list = []

    values_list = list(grouped_results.values())

    if return_count:
        return ceil(len(values_list) / 10)

    for i in range(0, 10):
        if ((page_number-1)*10 + i >= len(values_list)):
            break
        final_list.append(values_list[(page_number-1)*10 + i])

    return final_list


def get_routes_filtered(return_count:bool,page_number:int,db: Session, startCity: str, startCountry: str, endCity: str, endCountry: str, date: Optional[datetime.datetime],price_from:Optional[float] = None,price_to:Optional[float] = None,companyname = Optional[str]):
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
    if not companyname:
        companyname = ""
    

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

    routesIds = db.query(models.Route.id).filter(models.Route.arrival_station_id.in_(endStations)).filter(models.Route.departure_station_id.in_(startStations))

    routes_filtered: List = db.query(models.RouteDayAssociation, models.Company.company_name, models.RouteStationAssociation, models.Station,models.Company.id,models.Route.departure_time).\
        join(models.Route,models.RouteDay.route_id == models.Route.id).filter(models.Company.id == models.RouteDayAssociation.columns.get("company_id"),
               models.Route.id.in_(routesIds),                                                        
               models.RouteDayAssociation.columns.get(
               'route_id') == models.RouteStationAssociation.columns.get('route_id'),
               models.RouteStationAssociation.columns.get(
               'station_id') == models.Station.id,
               models.Route.is_active == 1,
               models.Route.price >= price_from,models.Route.price <= price_to,
               models.Company.company_name.like(f'%{companyname}%'),
               models.RouteDayAssociation.columns.get('day_name') == day_of_week_full).order_by(models.RouteStationAssociation.columns.get('id'))  \
        .all()
    grouped_results = {}

    for item in routes_filtered:
        route_id = item[1]
        if route_id not in grouped_results:
            grouped_results[route_id] = {
                "company_name": item[3],
                "stations": [],
                "route_id": item[1],
                "company_id":item[11],
                "departure_time":item[12]
            }
        if not find_station(grouped_results[route_id]["stations"], item[10]):
            grouped_results[route_id]["stations"].append({"station": item[10],
                                                          "arrival_time": item[8],
                                                          "departure_time": item[7],
                                                          "price": item[9]

                                                          })
    final_list = []

    values_list = sorted(grouped_results.values(), key=lambda x: x['departure_time'])
    if return_count:
        return ceil(len(values_list) / 10)

    for i in range(0, 10):
        if ((page_number-1)*10 + i >= len(values_list)):
            break
        final_list.append(values_list[(page_number-1)*10 + i])

    return final_list

# brisanje u smislu setanje  is_active na -1
def delete_routeID(db: Session, id: int, day_name: str, flag: Optional[bool] = None):

    route_to_find = db.query(models.Route).filter(
        models.Route.id == id).first()

    if not route_to_find:
        raise HTTPException(
            status_code=404, detail=f'Route with ID: {id} not found!')

    parent_route = route_to_find.parent_route
    arrival_station_id = route_to_find.arrival_station_id
    all_routes = []

    if flag:
        if parent_route:
            all_routes = db.query(models.Route).filter(or_(
                models.Route.parent_route == parent_route, models.Route.id == parent_route)).all()
        else:
            all_routes = db.query(models.Route).filter(
                or_(models.Route.parent_route == id, models.Route.id == id)).all()

        for route in all_routes:
            route.is_active = -1

        db.commit()
        return

    if parent_route:
        all_routes = db.query(models.Route).filter(or_(models.Route.parent_route == parent_route,
                                                       models.Route.id == parent_route), models.Route.arrival_station_id == arrival_station_id).all()
    else:
        all_routes = db.query(models.Route).filter(or_(models.Route.parent_route == id,
                                                       models.Route.id == id), models.Route.arrival_station_id == arrival_station_id).all()
    route = None
    if not day_name:
        for route in all_routes:
            route.is_active = -1


    else:
        all_routes_ids = [route.id for route in all_routes]
        to_delete = db.query(models.RouteDay).filter(models.RouteDayAssociation.columns.get("route_id").in_(all_routes_ids),models.RouteDayAssociation.get("day_name") == day_name)
        for route in to_delete:
            db.delete(to_delete)

    db.commit()


def create_route(days: List[models.Day], stations: List, company_id: int, db: Session):

    startStation = stations[0]
    endStation = stations[-1]
    parent_route_id = -1
    route_price = endStation.price

    new_route = models.Route(departure_station_id=startStation.station_id, arrival_station_id=endStation.station_id,
                             arrival_time=endStation.arrival_time, departure_time=startStation.departure_time, price=route_price, is_active=0)

    db.add(new_route)
    db.commit()
    parent_route_id = new_route.id

    for day in days:
        route_day = models.RouteDay(
            day_name=day.day_name, route_id=new_route.id, company_id=company_id)
        db.add(route_day)

    for k in range(0, len(stations)):
        station = stations[k]
        pricee = stations[k].price
        route_station = models.RouteStation(
            route_id=new_route.id,
            station_id=station.station_id,
            departure_time=station.departure_time,
            arrival_time=station.arrival_time,
            price=pricee
        )
        db.add(route_station)

    db.commit()

    for i in range(len(stations)):
        for j in range(i+1, len(stations)):

            if i == 0 and j == len(stations)-1:
                continue  # vec ubacena ruta

            startStation = stations[i]
            endStation = stations[j]

            route_price = endStation.price

            if (i != 0):
                route_price -= startStation.price

            new_route = models.Route(departure_station_id=startStation.station_id, arrival_station_id=endStation.station_id,
                                     arrival_time=endStation.arrival_time, departure_time=startStation.departure_time, price=route_price, is_active=0, parent_route=parent_route_id)

            db.add(new_route)
            db.commit()
            db.refresh(new_route)

            for day in days:
                route_day = models.RouteDay(
                    day_name=day.day_name, route_id=new_route.id, company_id=company_id)
                db.add(route_day)

            for k in range(i, j+1):
                station = stations[k]
                pricee = None
                if k != i:
                    if not startStation.price:
                        pricee = stations[k].price
                    else:
                        pricee = stations[k].price - startStation.price

                route_station = models.RouteStation(
                    route_id=new_route.id,
                    station_id=station.station_id,
                    departure_time=station.departure_time,
                    arrival_time=station.arrival_time,
                    price=pricee
                )
                db.add(route_station)

            db.commit()

    return new_route

def update(id: int, days: List[models.Day], stations: List, company_id: int, db: Session):
    delete_routeID(db,id,None,True)
    return create_route(days, stations, company_id, db)


def activate_deactivate(id: int, should_be_activated: bool, db: Session):
    if not should_be_activated:
        delete_routeID(db, id, None,True)

    else:
        route_to_update = db.query(models.Route).filter(
            models.Route.id == id).first()

        if not route_to_update:
            raise HTTPException(
            status_code=404, detail=f'Route with ID: {id} not found!')
        
        all_routes = db.query(models.Route).filter(models.Route.parent_route == id)

        route_to_update.is_active = 1
        for route in all_routes:
            route.is_active = 1
        
        db.commit()
        db.refresh(route_to_update)


def get_all_inactive(db: Session):
    routes = db.query(models.Route.id).filter(
        models.Route.is_active == 0).all()
    return [route[0] for route in routes]


def get_all_active(db: Session):
    routes = db.query(models.Route.id).filter(
        models.Route.is_active == 1).all()
    return [route[0] for route in routes]


def get_route_by_id(id: int, db: Session):
    routes_filtered = db.query(models.RouteDay.route_id, models.Company.company_name, models.RouteDay.day_name, models.RouteStationAssociation, models.Station,models.Company.id)\
        .filter(models.Company.id == models.RouteDay.company_id,
                models.RouteStationAssociation.columns.get(
                    "route_id") == models.RouteDay.route_id,
                models.RouteDay.route_id == id,
                models.Station.id == models.RouteStationAssociation.columns.get(
                    "station_id")
                ).order_by(models.RouteStationAssociation.columns.get(
                    "route_id")).all()

    grouped_results = {}
    seen_days = []

    for item in routes_filtered:
        route_id = item[0]

        if route_id not in grouped_results:
            grouped_results[route_id] = {
                "company_name": item[1],
                "stations": [],
                "route_id": item[0],
                "days": [],
                "company_id":item[10]
            }
        if not find_station(grouped_results[route_id]["stations"], item[9]):
            grouped_results[route_id]["stations"].append({"station": item[9],
                                                          "arrival_time": item[7],
                                                          "departure_time": item[6],
                                                          "price": item[8]
                                                          })
        if item[2] not in seen_days:
            grouped_results[route_id]["days"].append({"day_name": item[2]})
            seen_days.append(item[2])

    final_list = []

    for key, value in grouped_results.items():
        final_list.append(value)


    return final_list