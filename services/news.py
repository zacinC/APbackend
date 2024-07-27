

from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..MySql import models
import cloudinary.uploader
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from slugify import slugify
import datetime
from ..schemas import schemas


cloudinary.config( 
    cloud_name = "dj8zqugmr", 
    api_key = "813214989451761", 
    api_secret = "NzzFoCEy3NyriRGO_yiUGNlNByU",
    secure=True
)

def extract_public_id(image_url: str) -> str:
    return image_url.split('/')[-1].split('.')[0]

def get_news(db:Session):
    return db.query(models.News).all()

def upload_news(db: Session, notif: schemas.NewsCreate):

    print(notif.image)

    img = notif.image
    upload_result = cloudinary.uploader.upload(img)
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


def delete(db:Session,id:int):
    to_delete = db.query(models.News).filter(models.News.id == id).first()

    if not to_delete:
        raise HTTPException(status_code=404,detail="Not found!")

    image_url = to_delete.image
    public_id = extract_public_id(image_url)
    
    cloudinary.uploader.destroy(public_id)
    
    db.delete(to_delete)
    db.commit()

def update(db:Session,id:int,notif:schemas.NewsCreate):
    to_update = db.query(models.News).filter(models.News.id == id).first()
    if not to_update:
        raise HTTPException(status_code=404,detail="Not found!")
    
    image_url = to_update.image
    public_id = extract_public_id(image_url)

    print(public_id)
    
    cloudinary.uploader.destroy(public_id)

    img = notif.image
    upload_result = cloudinary.uploader.upload(img)
    upload_result_url = upload_result['url']

    to_update.content = notif.content
    to_update.title = notif.title
    to_update.created_date = notif.created_date
    to_slug = f"{notif.title}-{id}"
    to_update.slug = slugify(to_slug)
    to_update.image=upload_result_url

    db.commit()

    








    