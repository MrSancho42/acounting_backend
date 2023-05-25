from typing import Annotated

from fastapi import APIRouter, Body, status
from pydantic import BaseModel

from services_manager import group_service, group_budget_service
from domain import BudgetKinds

router = APIRouter(
    prefix='/group-record-budget-services',
    tags=['group-record-budget-services'],
    responses={404: {'description': 'Not found'}},
)


class GroupRecordBudgetModel(BaseModel):
    name: str
    limit: float
    currency: str
    kind: BudgetKinds


class GetGroupRecordBudget(GroupRecordBudgetModel):
    pk_group_budget: int


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_group: Annotated[int, Body(embed=True)],
    group_record_budget: GroupRecordBudgetModel
):
    group = group_service.read(pk_group)
    group_budget_service.create(
        from_group=group,
        **group_record_budget.dict()
    )


@router.get('/get-group-budget-records', response_model=list[GetGroupRecordBudget])
async def get_group_budget_records(pk_group: int):
    from_group = group_service.read(pk_group)
    return group_budget_service.get_group_budget_records(from_group)
