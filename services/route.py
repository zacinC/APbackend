from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..MySql import models
import datetime



def get_routes(db: Session):
    return db.query(models.Route).all()

def get_routes_filtered_by_company(db: Session, companyname: str):
    routes_filtered = db.query(models.RouteDay.route_id,models.Company.company_name,models.RouteDay.day_name,models.RouteStationAssociation,models.Station)\
    .filter(models.Company.id == models.RouteDay.company_id,models.Company.company_name == companyname,
            models.RouteStationAssociation.columns.get("route_id") == models.RouteDay.route_id,
            models.Station.id ==  models.RouteStationAssociation.columns.get("station_id")
            ).all()
   
    grouped_results = {}


    for item in routes_filtered:
        route_id = item[0]
        if route_id not in grouped_results:
            grouped_results[route_id] = {
                "company_name":item[1],
                "stations": [],
            }

        grouped_results[route_id]["stations"].append({"station":item[8],
                                                        "arrival_time":item[7],
                                                        "departure_time":item[6]                                                 
                                                        })

    final_list = []

    for key,value in grouped_results.items():
        final_list.append(value)
        

    print(final_list)

    return final_list


def get_routes_filtered(db:Session,startCity:str,startCountry:str,endCity:str,endCountry:str,date:Optional[datetime.datetime]):

    day_of_week_full = date.strftime('%A')
 
    startStations:List[models.Station] = db.query(models.Station).filter(
        models.Station.city_name == startCity,
        models.Station.country_name == startCountry
    ).all()

    endStations:List[models.Station] = db.query(models.Station).filter(
        models.Station.city_name == endCity,
        models.Station.country_name == endCountry
    ).all()

    startStations = [station.id for station in startStations]
    endStations = [station.id for station in endStations]

    print(startStations,endStations)
    routes: List[models.Route] = db.query(models.Route).filter(models.Route.departure_station_id.in_(startStations)).filter(models.Route.arrival_station_id.in_(endStations)).all()

    routesIds = [route.id for route in routes]

    routes_filtered:List = db.query(models.RouteDayAssociation,models.Company.company_name,models.RouteStationAssociation,models.Station).\
    filter(models.RouteDayAssociation.columns.get("route_id").in_(routesIds),models.Company.id == models.RouteDayAssociation.columns.get("company_id"),
           models.RouteDayAssociation.columns.get('route_id') == models.RouteStationAssociation.columns.get('route_id'),
           models.RouteStationAssociation.columns.get('station_id') == models.Station.id,
           models.RouteDayAssociation.columns.get('day_name') == day_of_week_full).order_by(models.RouteStationAssociation.columns.get('id'))  \
        .all()
    grouped_results = {}

    print(routes_filtered)

    for item in routes_filtered:
        route_id = item[1]
        if route_id not in grouped_results:
            grouped_results[route_id] = {
                "company_name": item[3],
                "stations": [],
            }

        grouped_results[route_id]["stations"].append({"station":item[9],
                                                      "arrival_time":item[8],
                                                      "departure_time":item[7]                                                 
                                                      })
    
    final_list = []

    for key,value in grouped_results.items():
        final_list.append(value)
        

    print(final_list)

    return final_list

def delete_routeID(db: Session, id: int,day_name:str):
    route = None
    if not day_name:
        route:models.Route = db.query(models.Route).filter(models.Route.id == id).first()

        
    else:
        route:models.Route = db.query(models.RouteDay).filter(models.RouteDay.route_id == id,models.RouteDay.day_name == models.Day.day_name).first()

        if not route:
            raise HTTPException(status_code=404, detail=f'Route with ID: {id} not found!')

        try:
            db.delete(route)
            db.commit()
            return {"detail": "Route deleted successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def create_route(days:List[models.Day],stations:List,company_id:int,db:Session): 
    print("arfkmsfdkfdskfsdkfsdkfsdkfsdkfdskfdskdfskfsdkfsdkfsdkfsdk",stations)
    startStation = stations[0]
    endStation =  stations[-1]

    new_route = models.Route(departure_station_id=startStation.station_id, arrival_station_id=endStation.station_id,arrival_time = endStation.arrival_time,departure_time = startStation.departure_time)
    
    db.add(new_route)
    db.commit()

    for day in days:
        route_day = models.RouteDay(day_name=day.day_name, route_id=new_route.id, company_id=company_id)
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


