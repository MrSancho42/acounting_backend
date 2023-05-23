from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel, Field

from services_manager import (
    user_service, business_service, business_record_service, bill_service, business_category_service
)
from domain import RecordKinds

router = APIRouter(
    prefix='/business-record-services',
    tags=['business-record-services'],
    responses={404: {'description': 'Not found'}},
)


class BusinessRecord(BaseModel):
    amount: float
    description: str
    currency: str
    kind: RecordKinds
    creation_time: datetime = datetime.now()


class GetBusinessRecord(BusinessRecord):
    pk_record: int


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_bill: Annotated[int, Body(embed=True)],
    pk_business: Annotated[int, Body(embed=True)],
    pk_category: Annotated[int, Body(embed=True)],
    business_record: BusinessRecord
):
    bill = bill_service.read(pk_bill)
    business = business_service.read(pk_business)
    business_record_service.create(
        from_bill=bill,
        from_business=business,
        from_business_category=business_category_service.read(1),
        **business_record.dict()
    )


@router.get('/get-business-records', response_model=list[GetBusinessRecord])
async def get_business_records(pk_business: int, pk_bill: int | None = None):
    business = business_service.read(pk_business)
    bill = None
    if pk_bill is not None:
        bill = bill_service.read(pk_bill)
    return business_record_service.get_business_records(from_business=business, from_bill=bill)

# @router.get('/read/{pk_business}', response_model=Business, status_code=status.HTTP_200_OK)
# async def read(pk_business: int):
#     business = business_service.read(pk_business)
#     return {
#         'pk_business': business.pk_business,
#         'business': business.name
#     }
#
#
# @router.patch('/update', status_code=status.HTTP_200_OK)
# async def update(business: Business):
#     business_service.update(business_service.read(business.pk_business), business.dict(exclude_unset=True))

