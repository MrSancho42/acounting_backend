from typing import Annotated

from fastapi import APIRouter, Body, status
from pydantic import BaseModel

from services_manager import group_service, group_budget_service, group_category_service
from domain import BudgetKinds

router = APIRouter(
    prefix='/group-category-budget-services',
    tags=['group-category-budget-services'],
    responses={404: {'description': 'Not found'}},
)


class GroupCategoryBudgetModel(BaseModel):
    name: str
    limit: float
    currency: str
    kind: BudgetKinds


class GetGroupCategoryBudget(GroupCategoryBudgetModel):
    pk_group_budget: int
    fk_group_category: int | None


class GetGroupRecordBudget(GroupCategoryBudgetModel):
    pk_group_budget: int


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_group: Annotated[int, Body(embed=True)],
    pk_category: Annotated[int, Body(embed=True)],
    group_category_budget: GroupCategoryBudgetModel
):
    group = group_service.read(pk_group)
    category = group_category_service.read(pk_category)
    group_budget_service.create(
        from_group=group,
        from_category=category,
        **group_category_budget.dict()
    )


@router.get('/get-group-budget-categories', response_model=list[GetGroupCategoryBudget])
async def get_group_budget_categories(pk_group: int):
    from_group = group_service.read(pk_group)
    return group_budget_service.get_group_budget_categories(from_group)
