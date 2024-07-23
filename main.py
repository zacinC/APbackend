
import json
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from MySql import database
from MySql import models
from MySql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# app = FastAPI()


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
    # uvicorn.run(app, port=8000, host='127.0.0.1')
else:
    configure()
