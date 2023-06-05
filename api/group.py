from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel, Field

from services_manager import user_service, group_service
from domain import User


router = APIRouter(
    prefix='/group-services',
    tags=['group-services'],
    responses={404: {'description': 'Not found'}},
)


class Group(BaseModel):
    name: str


class GroupWithId(Group):
    pk_group: int


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(pk_user: Annotated[int, Body(embed=True)], group: Group):
    group_service.create(
        owner=user_service.read(pk_user),
        **group.dict()
    )


@router.get('/get-groups', response_model=list[GroupWithId])
async def get_bills(pk_user: int):
    return group_service.get_groups(user_service.read(pk_user))


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update(group: GroupWithId):
    group_service.update(group_service.read(group.pk_group), group.dict(exclude_unset=True))

