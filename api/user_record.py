from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, status
from pydantic import BaseModel

from services_manager import user_record_service, bill_service, user_service, user_category_service
from domain import RecordKinds, UserCategory

router = APIRouter(
    prefix='/record-services',
    tags=['record-services'],
    responses={404: {'description': 'Not found'}},
)


class UserRecord(BaseModel):
    amount: float
    description: str
    currency: str
    kind: RecordKinds
    creation_time: datetime = datetime.now()


class GetRecord(UserRecord):
    pk_record: int
    fk_category: int
    category_name: str


class UpdateRecord(UserRecord):
    pk_record: int
    fk_category: int


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_bill: Annotated[int, Body(embed=True)],
    pk_category: Annotated[int, Body(embed=True)],
    record: UserRecord
):
    bill = bill_service.read(pk_bill)
    category = user_category_service.read(pk_category)
    user_record_service.create(
        from_bill=bill,
        from_user_category=category,
        **record.dict()
    )


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update(user_record: UpdateRecord):
    print(user_record)
    print(user_record_service.read(user_record.pk_record), user_record.dict(exclude_unset=True))
    user_record_service.update(
        user_record_service.read(user_record.pk_record), user_record.dict(exclude_unset=True)
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
    records = user_record_service.get_records(from_user=from_user, from_bill=from_bill)

    # add category name to result
    result = []
    for record in records:
        record['category_name'] = user_category_service.get_user_category_name(record['fk_category'])
        result.append(record)

    return result
