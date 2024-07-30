from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
import uvicorn

from .settings import ACCESS_TOKEN_EXPIRE_MINUTES
from .routers import user, role, route, city, country, station, ticket, news, login
from .MySql import models
from .MySql.database import SessionLocal, engine
from .schemas.schemas import UserBase, Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from .auth.utils import generate_password_reset_token
from .auth.deps import get_current_active_user
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def configure():
    configure_routing()


def configure_routing():
    app.include_router(user.user_router)
    app.include_router(role.role_router)
    app.include_router(route.route_router)
    app.include_router(city.city_router)
    app.include_router(country.country_router)
    app.include_router(station.station_router)
    app.include_router(ticket.ticket_router)
    app.include_router(news.news_router)
    app.include_router(login.login_router)


if __name__ == '__main__':
    configure()
    uvicorn.run(app, port=8000, host='127.0.0.1')
else:
    configure()
