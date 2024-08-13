import json
from math import ceil
import os
from pathlib import Path
from typing import Optional
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from database import models
import cloudinary.uploader
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from slugify import slugify
import datetime
from schemas import schemas
from settings import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET,PATH
from sqlalchemy import or_
from sqlalchemy import func
from sqlalchemy import desc
from pathlib import Path
import shutil



cloudinary.config(
    cloud_name="dj8zqugmr",
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

TEMP_DIR = PATH


def extract_public_id(image_url: str) -> str:
    return image_url.split('/')[-1].split('.')[0]


def get_news(db: Session, page_number):
    return db.query(models.News).order_by(desc(models.News.id)).offset((page_number-1)*10).limit(10).all()


def get_news_count(db: Session):
    return ceil(db.query(func.count(models.News.id)).scalar() / 10)


def get_news_filtered(db: Session, search: str, page_number: int):

    return db.query(models.News).filter(
        or_(
            models.News.content.like(f'%{search}%'),
            models.News.title.like(f'%{search}%')
        )
    ).order_by(desc(models.News.id)).offset((page_number-1)*10).limit(10).all()


def get_news_filtered_count(db: Session, search: str):

    news = db.query(models.News).filter(
        or_(
            models.News.content.like(f'%{search}%'),
            models.News.title.like(f'%{search}%')
        )
    ).all()

    return ceil(len(news) / 10)


def upload_news(db: Session, notif: schemas.NewsCreate):


    upload_result_url = None

    to_create = models.News(
        title=notif.title,
        content=notif.content,
        slug="",
        created_date=datetime.datetime.now(),
        image=upload_result_url
    )

    db.add(to_create)
    db.commit()
    db.refresh(to_create)

    to_slug = f"{notif.title}-{to_create.id}"
    slug = slugify(to_slug)

    to_create.slug = slug
    db.commit()
    db.refresh(to_create)

    return to_create


def delete(db: Session, id: int):
    to_delete = db.query(models.News).filter(models.News.id == id).first()

    if not to_delete:
        raise HTTPException(status_code=404, detail="Not found!")

    if to_delete.image:
        image_url = to_delete.image
        public_id = extract_public_id(image_url)

        cloudinary.uploader.destroy(public_id)

    db.delete(to_delete)
    db.commit()


def update(db: Session, id: int, notif: schemas.NewsCreate):
    to_update = db.query(models.News).filter(models.News.id == id).first()
    if not to_update:
        raise HTTPException(status_code=404, detail="Not found!")

    to_update.content = notif.content
    to_update.title = notif.title
    to_update.created_date = to_update.created_date
    to_slug = f"{notif.title}-{id}"
    to_update.slug = slugify(to_slug)

    db.commit()
    db.refresh(to_update)

    return to_update

def upload_img_id(id:int,db:Session,image:Optional[UploadFile]):
    to_update = db.query(models.News).filter(models.News.id == id).first()
    upload_result_url = None
    if not to_update:
        raise HTTPException(status_code=404, detail="Not found!")
    
    
    if to_update.image:
        image_url = to_update.image
        public_id = extract_public_id(image_url)
        cloudinary.uploader.destroy(public_id)


    if image:
        print("usao")
        temp_file_path = Path(TEMP_DIR + "/" + image.filename)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        try:
            result = cloudinary.uploader.upload(str(temp_file_path))
            upload_result_url = result.get("secure_url")
        finally:
            if temp_file_path.exists():
                os.remove(temp_file_path)

            to_update.image = upload_result_url
            db.commit()
            

    
    
    return to_update
            
