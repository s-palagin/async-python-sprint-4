from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class Activity(BaseModel):
    activity: datetime
    client: str
    link_id: int

    class Config:
        orm_mode = True


# Properties to receive on links creation
class LongLink(BaseModel):
    long_link: HttpUrl

    class Config:
        orm_mode = True


# Properties to return to client short_link
class ShortLink(BaseModel):
    id: int
    long_link: HttpUrl
    short_link: str

    class Config:
        orm_mode = True


class ClientActivity(BaseModel):
    client: str
    date: datetime


# Properties to return to client links status
class LinkStatus(BaseModel):
    id: int
    amount: int
    activity: Optional[list[ClientActivity]]
