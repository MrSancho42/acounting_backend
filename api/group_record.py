from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, status
from pydantic import BaseModel

from services_manager import group_record_service, bill_service, group_service, group_category_service
from domain import RecordKinds

router = APIRouter(
    prefix='/group_record-services',
    tags=['group-record-services'],
    responses={404: {'description': 'Not found'}},
)


class GroupRecord(BaseModel):
    amount: float
    description: str
    currency: str
    kind: RecordKinds
    creation_time: datetime = datetime.now()


class GetRecord(GroupRecord):
    pk_record: int


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_bill: Annotated[int, Body(embed=True)],
    pk_group: Annotated[int, Body(embed=True)],
    pk_category: Annotated[int, Body(embed=True)],
    record: GroupRecord
):
    bill = bill_service.read(pk_bill)
    category = group_category_service.read(pk_category)
    group = group_service.read(pk_group)
    group_record_service.create(
        from_bill=bill,
        from_group=group,
        from_group_category=category,
        **record.dict()
    )


@router.get('/get-group-records', response_model=list[GetRecord])
async def get_records(pk_group: int):
    from_group = group_service.read(pk_group)

    return group_record_service.get_group_records(from_group=from_group)
