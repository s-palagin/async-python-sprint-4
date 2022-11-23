from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class BaseWithORM(BaseModel):
    class Config:
        orm_mode = True


class Activity(BaseWithORM):
    activity: datetime
    client: str
    link_id: int


class LongLink(BaseWithORM):
    long_link: HttpUrl


class ShortLink(BaseWithORM):
    id: int
    long_link: HttpUrl
    short_link: str


class ClientActivity(BaseModel):
    client: str
    date: datetime


class LinkStatus(BaseModel):
    id: int
    amount: int
    activity: Optional[list[ClientActivity]]
