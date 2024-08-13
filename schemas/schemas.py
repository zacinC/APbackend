from decimal import Decimal
import uuid
from fastapi import File, UploadFile
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime, time

# News Schema


class NewsBase(BaseModel):

    title: str
    content: str
    is_active: bool = True
    created_date: datetime = datetime.now()
    image: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int
    slug: str
    


    class Config:
        orm_mode: True

# Role Schema


class RoleBase(BaseModel):
    type: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):

    class Config:
        orm_mode: True

# User Schema


class UserBase(BaseModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=30)
    full_name: str
    phone_number: str
    disabled: bool = True
    role_type: Optional[str] = Field(default="Passenger")



class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(BaseModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=30)
    full_name: str
    phone_number: str
    password: str = Field(min_length=8, max_length=40)
    role_type: str = "Passenger"
    company_id: Optional[int] = None


class UserUpdate(BaseModel):
    email: EmailStr = Field(unique=True, index=True,
                            max_length=255, default=None)
    username: str = Field(unique=True, index=True, max_length=30, default=None)
    full_name: str = None
    phone_number: str = None
    password: str = Field(min_length=8, max_length=40, default=None)
    role_type: str = None
    company_id: Optional[int] = None
    disabled: Optional[bool] = None


class User(UserBase):
    id: int
    hashed_password: str
    role_type: Optional[str] = Field(default="Passenger")
    company_id: Optional[int] = None
    company_name:Optional[str] = None
    tickets: List['Ticket'] = []

    class Config:
        orm_mode: True

# Properties to return via API, id is always required


class UserPublic(UserBase):
    id: int
    role_type: Optional[str] = Field(default="Passenger")
    company_id: Optional[int] = None
    company_name:Optional[str] = None
    tickets: List['Ticket'] = []

# Company Schema


class CompanyBase(BaseModel):
    company_name: str


class CompanyCreate(CompanyBase):
    pass

class CompanyShow(CompanyBase):
    id:int

class Company(CompanyBase):
    id: int
    users: List[User] = []

    class Config:
        orm_mode: True

# Ticket Schema


class TicketBase(BaseModel):
    price: float
    departure_date_time: datetime


class TicketCreate(TicketBase):
    company_id: int
    day_name: str
    route_id: int


class Ticket(TicketBase):
    id: int
    passenger_id: int
    company_id: int
    day_name: str
    route_id: int

    class Config:
        orm_mode: True

# Route Schema


class RouteBase(BaseModel):
    departure_time: time
    arrival_time: time
    price: Decimal
    is_active: Optional[int] = 0


class RouteCreate(RouteBase):
    departure_station_id: int
    arrival_station_id: int


class Route(RouteBase):
    id: int
    departure_station_id: int
    arrival_station_id: int
    tickets: List[Ticket] = []

    class Config:
        orm_mode: True

# Station Schema


class StationBase(BaseModel):
    phone_number: Optional[str]
    address: Optional[str]
    city_name: Optional[str]
    country_name: Optional[str]
    latitude: Optional[Decimal] = Field(None, max_digits=10, decimal_places=8)
    longitude: Optional[Decimal] = Field(None, max_digits=11, decimal_places=8)


class StationCreate(StationBase):
    city_name: str
    country_name: str

    class Config:
        orm_mode: True


class StationFormatted(StationBase):
    id: int


class Station(StationBase):
    id: int
    city_name: str
    country_name: str
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
    departure_time: time
    arrival_time: time

    class Config:
        orm_mode: True


class RouteStationCreate(RouteStationBase):
    pass


class RouteStation(RouteStationBase):
    pass

    class Config:
        orm_mode: True


class RouteStationFormatted(BaseModel):
    station: StationFormatted
    arrival_time: Optional[time]
    departure_time: Optional[time]
    price: Optional[float] = None

    class Config:
        orm_mode: True


class RouteResponse(BaseModel):  # za sve rute filtrirane
    stations: List[RouteStationFormatted]
    company_name: Optional[str]
    route_id: int
    days:Optional[List[DayBase]] = []
    company_id:int

    class Config:
        orm_mode: True


class RouteStation2(BaseModel):
    station_id: int
    departure_time: Optional[time] = None
    arrival_time: Optional[time] = None
    price: Optional[float] = None


class RouteCreateRequest(BaseModel):
    stations: List[RouteStation2]
    days: List[DayBase]

    class Config:
        orm_mode: True

# Token for auth


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

# Password format


class NewPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# Message
class Message(BaseModel):
    message: str