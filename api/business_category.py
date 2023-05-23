from typing import Annotated
from fastapi import APIRouter, Body, status
from pydantic import BaseModel

from services_manager import business_service, business_category_service

router = APIRouter(
    prefix='/business-category-services',
    tags=['business-category-services'],
    responses={404: {'description': 'Not found'}},
)


class BusinessCategoryModel(BaseModel):
    name: str
    ico: str
    colour: str


class GetBusinessCategory(BusinessCategoryModel):
    pk_business_category: int
    fk_parent_category: int | None = None


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_business: Annotated[int, Body(embed=True)],
    business_category: BusinessCategoryModel,
    pk_category: Annotated[int, Body(embed=True)] | None = None
):
    print(pk_category)
    business = business_service.read(pk_business)
    parent = None
    if pk_category:
        parent = business_category_service.read(pk_category)
    print(parent)
    business_category_service.create(
        from_business=business,
        from_parent=parent,
        **business_category.dict()
    )


@router.get('/get-business-categories', response_model=list[GetBusinessCategory])
async def get_business_categories(pk_business: int):
    from_business = business_service.read(pk_business)
    return business_category_service.get_business_categories(from_business)
