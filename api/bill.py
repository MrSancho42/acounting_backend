from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel, Field

from services_manager import user_service, bill_service

router = APIRouter(
    prefix='/bill-services',
    tags=['bill-services'],
    responses={404: {'description': 'Not found'}},
)


class CreateBill(BaseModel):
    name: str
    amount: float
    currency: str
    is_for_business: bool


class Bill(BaseModel):
    pk_bill: int
    name: str
    amount: float
    currency: str
    is_for_business: bool


class UpdateBill(BaseModel):
    pk_bill: int
    name: str = None
    amount: float = None
    currency: str = None
    is_for_business: bool = None


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(pk_user: Annotated[int, Body(embed=True)], bill: CreateBill):
    print("Create Bill >>> ", bill)
    bill_service.create(
        owner=user_service.read(pk_user),
        **bill.dict()
    )


@router.get('/read/{pk_bill}', response_model=Bill, status_code=status.HTTP_200_OK)
async def read(pk_bill: int):
    bill = bill_service.read(pk_bill)
    return {
        'pk_bill': bill.pk_bill,
        'name': bill.name,
        'amount': bill.amount,
        'currency': bill.currency,
        'is_for_business': bill.is_for_business
    }


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update(bill: UpdateBill):
    bill_service.update(bill_service.read(bill.pk_bill), bill.dict(exclude_unset=True))


@router.get('/get-bills', response_model=list[Bill])
async def get_bills(pk_user: int, for_business: bool = False):
    return bill_service.get_bills(user_service.read(pk_user), for_business=for_business)
