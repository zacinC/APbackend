from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from .routers import user, role, route, city, country, station, ticket, news, login
from .database import models
from .database.dbconfig import engine

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
    configure_exceptions()


def configure_exceptions():
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {"detail": exc.errors(), "body": exc.body}),
        )


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
