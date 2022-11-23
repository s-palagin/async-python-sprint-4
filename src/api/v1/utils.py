from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.link import RepositoryLink


async def get_db_obj(db: AsyncSession, crud: RepositoryLink, id: int) -> Any:
    if answer := await crud.get(db=db, id=id):
        return answer
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found"
    )
