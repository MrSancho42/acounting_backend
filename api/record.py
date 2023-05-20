from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, status
from pydantic import BaseModel

from services_manager import record_service, bill_service, user_service
from domain import RecordKinds

router = APIRouter(
    prefix='/record-services',
    tags=['record-services'],
    responses={404: {'description': 'Not found'}},
)


class Record(BaseModel):
    amount: float
    description: str
    currency: str
    kind: RecordKinds
    creation_time: datetime = datetime.now()


class GetRecord(Record):
    pk_record: int


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_bill: Annotated[int, Body(embed=True)],
    record: Record
):
    bill = bill_service.read(pk_bill)
    record_service.create(
        from_bill=bill,
        **record.dict()
    )


@router.get('/get-records', response_model=list[GetRecord])
async def get_records(pk_user: int | None = None, pk_bill: int | None = None):
    from_user, from_bill = None, None

    if pk_user is not None and pk_bill is None:
        # define user
        from_user = user_service.read(pk_user)
    elif pk_user is None and pk_bill is not None:
        # or define bill
        from_bill = bill_service.read(pk_bill)
    return record_service.get_records(from_user=from_user, from_bill=from_bill)
