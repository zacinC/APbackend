from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(String(5000))
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime)


class Role(Base):
    __tablename__ = "role"

    type = Column(String(10), primary_key=True, index=True)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, index=True)
    name = Column(String(20))
    lastname = Column(String(35))
    hashed_password = Column(String(200))
    phone_number = Column(String(25))
    company_id = Column(Integer, ForeignKey("company.id"))
    role_type = Column(String(10), ForeignKey("role.type"))

    role = relationship("Role", back_populates="users")
    company = relationship("Company", back_populates="users")
    tickets = relationship("Ticket", back_populates="user")


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    company_name = Column(String(25))

    users = relationship("User", back_populates="company")


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True)
    price = Column(Double)
    departure_date_time = Column(DateTime)
    passenger_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("routeday.company_id"))
    day_name = Column(String(10), ForeignKey("routeday.day_name"))
    route_id = Column(Integer, ForeignKey("routeday.route_id"))

    routeday = relationship("RouteDay", back_populates="tickets")
    user = relationship("User", back_populates="tickets")


class Route(Base):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    departure_station_id = Column(Integer, ForeignKey("station.id"))
    arrival_station_id = Column(Integer, ForeignKey("station.id"))

    tickets = relationship("Ticket", back_populates="routeday")
    days = relationship("Day", secondary='routeday', back_populates='routes')
    stations = relationship(
        "Station", secondary='routestation', back_populates='routes')
# Treba srediti vise u vise vezu izmedju route i station


class Station(Base):
    __tablename__ = "station"

    id = Column(Integer, primary_key=True)
    address = Column(String(25))
    city_name = Column(String(25), ForeignKey("city.city_name"))
    country_name = Column(String(25), ForeignKey("country.country_name"))

    city = relationship("City", back_populates="stations")
    routes = relationship("Route", secondary='routestation',
                          back_populates="stations")


class City(Base):
    __tablename__ = "city"

    city_name = Column(String(20), primary_key=True)
    country_name = Column(String(20), ForeignKey("country.country_name"))
    stations = relationship("Station", back_populates="city")
    country = relationship("Country", back_populates="cities")


class Country(Base):
    __tablename__ = "country"

    country_name = Column(String(20), primary_key=True)

    cities = relationship("City", back_populates="country")


class Day(Base):
    __tablename__ = "day"

    day_name = Column(String(10), primary_key=True, index=True)
    routes = relationship('Route', secondary='routeday', back_populates='day')


class RouteDay(Base):
    __tablename__ = "routeday"
    day_name = Column(String(10), ForeignKey("day.day_name"), primary_key=True)
    route_id = Column(Integer, ForeignKey("route.id"), primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id"), primary_key=True)

    company = relationship("Company", back_populates="routes")
    tickets = relationship("Ticket", back_populates="routeday")


class RouteStation(Base):
    __tablename__ = "routestation"
    route_id = Column(Integer, ForeignKey("route.id"), primary_key=True)
    station_id = Column(Integer, ForeignKey("station.id"), primary_key=True)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
