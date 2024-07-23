from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
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
    tickets = relationship("Ticket", back_populates="company")


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True)
    price = Column(Double)
    departure_date_time = Column(DateTime)
    passenger_id = Column(Integer, ForeignKey("users"))
    company_id = Column(Integer, ForeignKey("company"))
    route_id = Column(Integer, ForeignKey("route"))

    route = relationship("Route", back_populates="tickets")
    user = relationship("User", back_populates="tickets")
    company = relationship("Company", back_populates="tickets")


class Route(Base):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    departure_station_id = Column(Integer, ForeignKey("station"))
    arrival_station_id = Column(Integer, ForeignKey("station"))

    tickets = relationship("Ticket", back_populates="route")
# Treba srediti vise u vise vezu izmedju route i station


class Station(Base):
    __tablename__ = "station"

    id = Column(Integer, primary_key=True)
    address = Column(String(25))
    city_name = Column(String(25), ForeignKey("city.name"))
    country_name = Column(String(25), ForeignKey("country.name"))

    city = relationship("City", back_populates="stations")


class City(Base):
    __tablename__ = "city"

    city_name = Column(String(20), primary_key=True)

    stations = relationship("Station", back_populates="city")
    country = relationship("Country", back_populates="cities")


class Country(Base):
    __tablename__ = "country"

    country_name = Column(String(20), primary_key=True)

    cities = relationship("City", back_populates="country")
