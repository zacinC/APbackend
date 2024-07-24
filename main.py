
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uvicorn

from .routers import user,role,route

from .MySql import models
from .MySql.database import SessionLocal, engine
from .schemas import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def configure():
    configure_routing()


def configure_routing():
    app.include_router(user.user_router)
    app.include_router(role.role_router)
    app.include_router(route.route_router)


if __name__ == '__main__':
    configure()
    uvicorn.run(app, port=8000, host='127.0.0.1')
else:
    configure()
