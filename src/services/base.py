from datetime import datetime
from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from ..db.db import Base
from ..utils.settings import LINK_LENGTH
from .utils import get_short_link


class Repository:
    def add(self, *args, **kwargs):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise NotImplementedError


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class RepositoryDBActivity(Repository, Generic[ModelType, CreateSchemaType]):
    def __init__(self, activity_model: Type[ModelType]) -> None:
        self._acttivity_model = activity_model

    async def add(self, id: int, client: str, db: AsyncSession) -> None:
        new_activity = {
            'activity': datetime.now(),
            'client': client,
            'link_id': id
        }
        db_obj = self._acttivity_model(**new_activity)
        db.add(db_obj)
        await db.commit()

    async def get_full(
        self, db: AsyncSession, id: int, skip: int = 0, limit: int = 100
    ) -> Any:
        statement = select(
            self._acttivity_model).where(
            self._acttivity_model.link_id == id).offset(skip).limit(limit)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def get(self, db: AsyncSession, id: int) -> Any:
        statement = select(
            self._acttivity_model).where(
            self._acttivity_model.link_id == id).with_only_columns(
            [func.count()])
        result = await db.execute(statement=statement)
        return result.scalar()


class RepositoryDBLink(Repository, Generic[ModelType, CreateSchemaType]):
    def __init__(self, links_model: Type[ModelType]):
        self._links_model = links_model

    async def add(
        self, db: AsyncSession, obj_in: list[CreateSchemaType]
    ) -> list[ModelType]:
        obj_in_data = jsonable_encoder(obj_in)
        answer = []
        for data in obj_in_data:
            data['short_link'] = get_short_link(LINK_LENGTH)
            db_obj = self._links_model(**data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            answer.append(db_obj)
        return answer

    async def get(self, id: int, db: AsyncSession) -> Any:
        statement = select(self._links_model).where(self._links_model.id == id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def delete(self, db: AsyncSession, db_obj: ModelType) -> None:
        setattr(db_obj, 'is_deleted', True)
        await db.commit()
