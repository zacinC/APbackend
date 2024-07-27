from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
import uvicorn

from .settings import ACCESS_TOKEN_EXPIRE_MINUTES
from .routers import user, role, route, city, country, station, ticket
from .MySql import models
from .MySql.database import SessionLocal, engine
from .schemas.schemas import UserBase, Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from .auth.security import authenticate_user, create_access_token
from .auth.deps import get_current_active_user

# Initialize the CryptContext with bcrypt scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    db = SessionLocal()
    try:
        user = await authenticate_user(
            form_data.username, form_data.password, db
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    finally:
        db.close()


@app.get("/users/me", response_model=UserBase)
async def read_users_me(
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


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


if __name__ == '__main__':
    configure()
    uvicorn.run(app, port=8000, host='127.0.0.1')
else:
    configure()
