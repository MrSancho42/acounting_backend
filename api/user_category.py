from typing import Annotated

from fastapi import APIRouter, Body, status
from pydantic import BaseModel

from services_manager import user_service, user_category_service

router = APIRouter(
    prefix='/user-category-services',
    tags=['user-category-services'],
    responses={404: {'description': 'Not found'}},
)


class UserCategoryModel(BaseModel):
    name: str
    ico: str
    colour: str


class GetUserCategory(UserCategoryModel):
    pk_user_category: int
    fk_parent_category: int | None


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_user: Annotated[int, Body(embed=True)],
    pk_category: Annotated[int, Body(embed=True)],
    user_category: UserCategoryModel
):
    user = user_service.read(pk_user)
    parent = None
    if pk_category:
        parent = user_category_service.read(pk_category)
    user_category_service.create(
        from_user=user,
        from_parent=parent,
        **user_category.dict()
    )


@router.get('/get-user-categories', response_model=list[GetUserCategory])
async def get_user_categories(pk_user: int):
    from_user = user_service.read(pk_user)
    return user_category_service.get_user_categories(from_user)
