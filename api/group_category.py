from typing import Annotated

from fastapi import APIRouter, Body, status
from pydantic import BaseModel

from services_manager import group_service, group_category_service

router = APIRouter(
    prefix='/group-category-services',
    tags=['group-category-services'],
    responses={404: {'description': 'Not found'}},
)


class GroupCategoryModel(BaseModel):
    name: str
    ico: str
    colour: str


class GetGroupCategory(GroupCategoryModel):
    pk_group_category: int
    fk_parent_category: int | None


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_group: Annotated[int, Body(embed=True)],
    pk_category: Annotated[int, Body(embed=True)],
    group_category: GroupCategoryModel
):
    group = group_service.read(pk_group)
    parent = None
    if pk_category:
        parent = group_category_service.read(pk_category)
    group_category_service.create(
        from_group=group,
        from_parent=parent,
        **group_category.dict()
    )


@router.get('/get-group-categories', response_model=list[GetGroupCategory])
async def get_group_categories(pk_group: int):
    from_group = group_service.read(pk_group)
    return group_category_service.get_group_categories(from_group)
