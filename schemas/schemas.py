from pydantic import BaseModel
import datetime


class NewsBase(BaseModel):
    title: str
    content: str
    is_active: bool
    created_date: datetime.datetime


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int

    class Config:
        orm_mode = True
