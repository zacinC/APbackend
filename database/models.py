from sqlalchemy import DECIMAL, Boolean, Column, ForeignKey, ForeignKeyConstraint, Integer, String, DateTime, Double, Table, Time
from sqlalchemy.orm import relationship

from .dbconfig import Base


RouteDayAssociation = Table(
    'routeday',
    Base.metadata,
    Column('day_name', String(10), ForeignKey(
        'day.day_name'), primary_key=True),
    Column('route_id', Integer, ForeignKey('route.id'), primary_key=True),
    Column('company_id', Integer, ForeignKey('company.id'), primary_key=True)
)

RouteStationAssociation = Table(
    'routestation',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('route_id', Integer, ForeignKey('route.id')),
    Column('station_id', Integer, ForeignKey('station.id')),
    Column('departure_time', Time, nullable=True),
    Column('arrival_time', Time, nullable=True),
    Column('price', DECIMAL(5, 2))
)


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(String(5000))
    is_active = Column(Boolean,default=True)
    created_date = Column(DateTime)
    image = Column(String(200))
    slug = Column(String(200))


class Role(Base):
    __tablename__ = "role"

    type = Column(String(10), primary_key=True, index=True)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, index=True)
    username = Column(String(20), unique=True)
    full_name = Column(String(35))
    hashed_password = Column(String(200))
    phone_number = Column(String(25))
    disabled = Column(Boolean, default=True)
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
    routes = relationship("RouteDay", back_populates="company")


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True)
    price = Column(Double)
    departure_date_time = Column(DateTime)
    passenger_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("routeday.company_id"))
    day_name = Column(String(10), ForeignKey("routeday.day_name"))
    route_id = Column(Integer, ForeignKey("routeday.route_id"))

    routeday = relationship(
        "RouteDay",
        primaryjoin="and_(Ticket.company_id == RouteDay.company_id, "
                    "Ticket.day_name == RouteDay.day_name, "
                    "Ticket.route_id == RouteDay.route_id)",
        foreign_keys="[Ticket.company_id, Ticket.day_name, Ticket.route_id]",
        back_populates="tickets"
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ['company_id', 'day_name', 'route_id'],
            ['routeday.company_id', 'routeday.day_name', 'routeday.route_id']
        ),
    )

    user = relationship("User", back_populates="tickets")


class Route(Base):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True)
    departure_time = Column(Time)
    arrival_time = Column(Time)
    departure_station_id = Column(Integer, ForeignKey("station.id"))
    arrival_station_id = Column(Integer, ForeignKey("station.id"))
    price = Column(DECIMAL(5, 2))
    is_active = Column(Integer)
    parent_route = Column(Integer,nullable=True)

    days = relationship("Day", secondary=RouteDayAssociation,
                        back_populates='routes')
    stations = relationship(
        "Station", secondary=RouteStationAssociation, back_populates='routes')


class Station(Base):
    __tablename__ = "station"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(25))
    address = Column(String(50))
    city_name = Column(String(25), ForeignKey("city.city_name"))
    country_name = Column(String(25), ForeignKey("country.country_name"))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))

    city = relationship("City", back_populates="stations")
    routes = relationship("Route", secondary=RouteStationAssociation,
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
    routes = relationship(
        'Route', secondary=RouteDayAssociation, back_populates='days')


class RouteDay(Base):
    __table__ = RouteDayAssociation

    company = relationship("Company", back_populates="routes")
    tickets = relationship(
        "Ticket",
        primaryjoin="and_(RouteDay.company_id == Ticket.company_id, "
                    "RouteDay.day_name == Ticket.day_name, "
                    "RouteDay.route_id == Ticket.route_id)",
        foreign_keys="[Ticket.company_id, Ticket.day_name, Ticket.route_id]",
        back_populates="routeday",
        cascade="all, delete-orphan"
    )


class RouteStation(Base):
    __table__ = RouteStationAssociation
