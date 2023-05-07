from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel, Field

from services_manager import user_service, business_service

router = APIRouter(
    prefix='/business-services',
    tags=['business-services'],
    responses={404: {'description': 'Not found'}},
)


class CreateBusiness(BaseModel):
    name: str


class Business(BaseModel):
    pk_business: int
    name: str


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(pk_user: Annotated[int, Body(embed=True)], business: CreateBusiness):
    business_service.create(business.name, user_service.read(pk_user))
    

@router.get('/read/{pk_business}', response_model=Business, status_code=status.HTTP_200_OK)
async def read(pk_business: int):
    business = business_service.read(pk_business)
    return {
        'pk_business': business.pk_business,
        'business': business.name
    }


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update(business: Business):
    business_service.update(business_service.read(business.pk_business), business.dict(exclude_unset=True))


@router.get('/get-businesses', response_model=list[Business])
async def get_businesses(pk_user: int):
    return business_service.get_businesses(user_service.read(pk_user))
