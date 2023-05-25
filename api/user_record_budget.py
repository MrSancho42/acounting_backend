from typing import Annotated

from fastapi import APIRouter, Body, status
from pydantic import BaseModel

from services_manager import user_service, user_budget_service
from domain import BudgetKinds

router = APIRouter(
    prefix='/user-record-budget-services',
    tags=['user-record-budget-services'],
    responses={404: {'description': 'Not found'}},
)


class UserRecordBudgetModel(BaseModel):
    name: str
    limit: float
    currency: str
    kind: BudgetKinds


class GetUserRecordBudget(UserRecordBudgetModel):
    pk_user_budget: int


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_user: Annotated[int, Body(embed=True)],
    user_record_budget: UserRecordBudgetModel
):
    user = user_service.read(pk_user)
    user_budget_service.create(
        from_user=user,
        **user_record_budget.dict()
    )


@router.get('/get-user-budget-records', response_model=list[GetUserRecordBudget])
async def get_user_budget_records(pk_user: int):
    from_user = user_service.read(pk_user)
    return user_budget_service.get_user_budget_records(from_user)
