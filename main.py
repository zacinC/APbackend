
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import uvicorn

from .services import auth
from .services.user import get_user_by_username

from .routers import user, role, route, city, country, station, ticket,news

from .MySql import models
from .MySql.database import SessionLocal, engine, get_db
from .schemas import schemas

from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def read_user(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_username_sync(username: str):
    db = SessionLocal()
    try:
        user = get_user_by_username(db, username)
        if user is None:
            print("User not found")
        else:
            # Convert user object to a dictionary
            user_dict = vars(user)
            return schemas.UserCreate(**user_dict)
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = get_user_by_username_sync(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user_by_username_sync(form_data.username)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[schemas.UserBase, Depends(get_current_user)]
):
    return current_user


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


if __name__ == '__main__':
    configure()
    uvicorn.run(app, port=8000, host='127.0.0.1')
else:
    configure()
