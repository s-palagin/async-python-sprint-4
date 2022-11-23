from typing import Any

from fastapi import APIRouter, Depends, Query, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from services.link import activity_crud, link_crud
from schemas import links as link_schema
from .utils import get_db_obj

router = APIRouter()


@router.get(
    "/{id}/status",
    response_model=link_schema.LinkStatus,
    response_model_exclude_unset=True
)
async def get_acivity(
    id: int,
    db: AsyncSession = Depends(get_session),
    full: bool = Query(False, alias='full-info'),
    skip: int = Query(0, alias='offset'),
    limit: int = Query(100, alias='max-result')
) -> link_schema.LinkStatus:
    await get_db_obj(db=db, crud=link_crud, id=id)
    amount = await activity_crud.get(db=db, id=id)
    answer = link_schema.LinkStatus(id=id, amount=amount)
    if full:
        results = await activity_crud.get_full(
            db=db, id=id, skip=skip, limit=limit)
        activity = []
        for result in results:
            activity.append(link_schema.ClientActivity(
                client=result.client,
                date=result.activity
            ))
        answer.activity = activity
    return answer


@router.get("/{id}", response_class=RedirectResponse)
async def get_link(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_session),
) -> Any:
    answer = await get_db_obj(db=db, crud=link_crud, id=id)
    if answer.is_deleted:
        return Response(status_code=status.HTTP_410_GONE)
    if request.client:
        client_adress = f'{request.client.host}:{request.client.port}'
        await activity_crud.add(id=id, client=client_adress, db=db)
    return answer.long_link


@router.delete("/{id}")
async def delete_link(
    id: int,
    db: AsyncSession = Depends(get_session)
) -> Response:
    answer = await get_db_obj(db=db, crud=link_crud, id=id)
    if answer.is_deleted:
        return Response(status_code=status.HTTP_410_GONE)
    await link_crud.delete(db=db, db_obj=answer)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=list[link_schema.ShortLink]
)
async def create_links(
    link_in: list[link_schema.LongLink],
    db: AsyncSession = Depends(get_session),
) -> Any:
    answer = await link_crud.add(db=db, obj_in=link_in)
    return answer
