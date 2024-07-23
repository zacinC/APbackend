
import json
from pathlib import Path
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from .MySql import models
from .MySql.database import SessionLocal, engine
from .schemas import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def configure():
    pass



if __name__ == '__main__':
    configure()
    uvicorn.run(app, port=8000, host='127.0.0.1')
else:
    configure()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

