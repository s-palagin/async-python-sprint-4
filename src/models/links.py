from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base: Any = declarative_base()


class Links(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    long_link = Column(String(2083), nullable=False)
    short_link = Column(String(8), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    activity: relationship = relationship('LinksActivity')


class LinksActivity(Base):
    __tablename__ = 'links_activity'
    id = Column(Integer, primary_key=True)
    activity = Column(DateTime, default=datetime.utcnow)
    client = Column(String(20), nullable=False)
    link_id = Column(Integer, ForeignKey('links.id'))
