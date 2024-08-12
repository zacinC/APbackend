from io import BytesIO
import json
from math import ceil
from pathlib import Path
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import models
import cloudinary.uploader
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from slugify import slugify
import datetime
from schemas import schemas
from settings import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from sqlalchemy import or_
from sqlalchemy import func
from sqlalchemy import desc


cloudinary.config(
    cloud_name="dj8zqugmr",
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)


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


async def upload_news(db: Session, notif: schemas.NewsCreate):


    upload_result_url = None

    if notif.image:
        img_bytes = BytesIO(await notif.image.read()) 
        upload_result = cloudinary.uploader.upload(img_bytes)
        upload_result_url = upload_result['url']

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

    image_url = to_update.image

    if (image_url):
        public_id = extract_public_id(image_url)


        cloudinary.uploader.destroy(public_id)

    upload_result_url = None

    if notif.image:
        img = notif.image
        upload_result_url = None
    if(img):
        upload_result = cloudinary.uploader.upload(img)
        upload_result_url = upload_result['url']

    to_update.content = notif.content
    to_update.title = notif.title
    to_update.created_date = to_update.created_date
    to_slug = f"{notif.title}-{id}"
    to_update.slug = slugify(to_slug)
    to_update.image = upload_result_url

    db.commit()
    db.refresh(to_update)

    return to_update
