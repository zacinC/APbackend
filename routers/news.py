
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter

from ..database.dbconfig import get_db
from ..services.news import get_news, upload_news, delete, update
from ..schemas import schemas

news_router = APIRouter()


@news_router.get("/news", response_model=List[schemas.News], tags=["news"])
def get_all_news(db: Session = Depends(get_db)):
    return get_news(db)


@news_router.post("/news", response_model=schemas.News, tags=["news"])
def add(notif: schemas.NewsCreate, db: Session = Depends(get_db)):
    return upload_news(db=db, notif=notif)


@news_router.delete("/news/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["news"])
def delete_news(id: int, db: Session = Depends(get_db)):
    return delete(db=db, id=id)


@news_router.put("/news/{id}", response_model=schemas.News, tags=["news"])
def update_news(notif: schemas.NewsCreate, id: int, db: Session = Depends(get_db)):
    return update(db=db, id=id, notif=notif)
