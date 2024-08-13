
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, File, HTTPException, UploadFile, status
from fastapi import APIRouter

from auth.deps import get_current_admin_user

from database.dbconfig import get_db
from services.news import get_news, upload_news, delete, update, get_news_filtered, get_news_count, get_news_filtered_count,upload_img_id
from schemas import schemas

news_router = APIRouter()


@news_router.get("/news/count", response_model=int, tags=["news"])
def get_all_news_count(db: Session = Depends(get_db)):
    return get_news_count(db)


@news_router.get("/news/{page_number}", response_model=List[schemas.News], tags=["news"])
def get_all_news(page_number: int, db: Session = Depends(get_db)):
    return get_news(db, page_number)


@news_router.get("/news-filtered/count", response_model=int, tags=["news"])
def get_all_news_filtered_count(search: str, db: Session = Depends(get_db)):
    return get_news_filtered_count(db, search)


@news_router.get("/news-filtered/{page_number}", response_model=List[schemas.News], tags=["news"])
def get_all_news_filtered(page_number: int, search: str, db: Session = Depends(get_db)):
    return get_news_filtered(db, search, page_number)


@news_router.post("/news", response_model=schemas.News, tags=["news"])
def add(current_user: Annotated[schemas.User, Depends(get_current_admin_user)],notif: schemas.NewsCreate,db: Session = Depends(get_db)):
    return upload_news(db=db, notif=notif)


@news_router.delete("/news/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["news"])
def delete_news(current_user: Annotated[schemas.User, Depends(get_current_admin_user)], id: int, db: Session = Depends(get_db)):
    return delete(db=db, id=id)


@news_router.put("/news/{id}", response_model=schemas.News, tags=["news"])
def update_news(current_user: Annotated[schemas.User, Depends(get_current_admin_user)], notif: schemas.NewsCreate, id: int, db: Session = Depends(get_db)):
    return update(db=db, id=id, notif=notif)

@news_router.put("/news/uploadimg/{id}",response_model=schemas.News,tags = ["news"])
def upload_img(current_user: Annotated[schemas.User, Depends(get_current_admin_user)],id:int,image:Optional[UploadFile] = File(None),db:Session = Depends(get_db)):
    return upload_img_id(id = id,db = db,image = image)

