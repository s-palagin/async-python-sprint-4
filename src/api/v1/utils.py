from fastapi import HTTPException, status

from ...services.link import link_crud


async def get_db_obj(db, id):
    answer = await link_crud.get(db=db, id=id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return answer
