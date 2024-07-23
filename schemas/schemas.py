from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# News Schema


class NewsBase(BaseModel):
    title: str
    content: str
    is_active: bool = True
    created_date: datetime = None


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int

    class Config:
        orm_mode: True

# Role Schema


class RoleBase(BaseModel):
    type: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    users: List['User'] = []

    class Config:
        orm_mode: True

# User Schema


class UserBase(BaseModel):
    email: EmailStr
    name: str
    lastname: str
    phone_number: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role_type: str
    company_id: Optional[int] = None
    role: Optional[Role] = None
    company: Optional['Company'] = None
    tickets: List['Ticket'] = []

    class Config:
        orm_mode: True

# Company Schema


class CompanyBase(BaseModel):
    company_name: str


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    users: List[User] = []
    tickets: List['Ticket'] = []
    routes: List['Route'] = []

    class Config:
        orm_mode: True

# Ticket Schema


class TicketBase(BaseModel):
    price: float
    departure_date_time: datetime


class TicketCreate(TicketBase):
    passenger_id: int
    company_id: int
    day_name: str
    route_id: int


class Ticket(TicketBase):
    id: int
    passenger_id: int
    company_id: int
    day_name: str
    route_id: int
    routeday: Optional['RouteDay'] = None
    user: Optional[User] = None

    class Config:
        orm_mode: True

# Route Schema


class RouteBase(BaseModel):
    departure_time: datetime
    arrival_time: datetime


class RouteCreate(RouteBase):
    departure_station_id: int
    arrival_station_id: int


class Route(RouteBase):
    id: int
    departure_station_id: int
    arrival_station_id: int
    tickets: List[Ticket] = []
    days: List['Day'] = []
    stations: List['Station'] = []

    class Config:
        orm_mode: True

# Station Schema


class StationBase(BaseModel):
    address: str


class StationCreate(StationBase):
    city_name: str
    country_name: str


class Station(StationBase):
    id: int
    city_name: str
    country_name: str
    city: Optional['City'] = None
    routes: List[Route] = []

    class Config:
        orm_mode: True

# City Schema


class CityBase(BaseModel):
    city_name: str


class CityCreate(CityBase):
    country_name: str


class City(CityBase):
    country_name: str
    stations: List[Station] = []
    country: Optional['Country'] = None

    class Config:
        orm_mode: True

# Country Schema


class CountryBase(BaseModel):
    country_name: str


class CountryCreate(CountryBase):
    pass


class Country(CountryBase):
    cities: List[City] = []

    class Config:
        orm_mode: True

# Day Schema


class DayBase(BaseModel):
    day_name: str


class DayCreate(DayBase):
    pass


class Day(DayBase):
    routes: List[Route] = []

    class Config:
        orm_mode: True

# RouteDay Schema


class RouteDayBase(BaseModel):
    day_name: str
    route_id: int
    company_id: int


class RouteDayCreate(RouteDayBase):
    pass


class RouteDay(RouteDayBase):
    company: Optional[Company] = None
    tickets: List[Ticket] = []

    class Config:
        orm_mode: True

# RouteStation Schema


class RouteStationBase(BaseModel):
    route_id: int
    station_id: int
    departure_time: datetime
    arrival_time: datetime


class RouteStationCreate(RouteStationBase):
    pass


class RouteStation(RouteStationBase):
    pass

    class Config:
        orm_mode: True
