from typing import Annotated

from fastapi import APIRouter, Body, status
from pydantic import BaseModel

from services_manager import user_service, user_budget_service, user_category_service
from domain import BudgetKinds

router = APIRouter(
    prefix='/user-category-budget-services',
    tags=['user-category-budget-services'],
    responses={404: {'description': 'Not found'}},
)


class UserCategoryBudgetModel(BaseModel):
    name: str
    limit: float
    currency: str
    kind: BudgetKinds


class GetUserCategoryBudget(UserCategoryBudgetModel):
    pk_user_budget: int
    fk_user_category: int | None


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    pk_user: Annotated[int, Body(embed=True)],
    pk_category: Annotated[int, Body(embed=True)],
    user_category_budget: UserCategoryBudgetModel
):
    user = user_service.read(pk_user)
    category = user_category_service.read(pk_category)
    user_budget_service.create(
        from_user=user,
        from_category=category,
        **user_category_budget.dict()
    )


@router.get('/get-user-budget-categories', response_model=list[GetUserCategoryBudget])
async def get_user_budget_categories(pk_user: int):
    from_user = user_service.read(pk_user)
    return user_budget_service.get_user_budget_categories(from_user)
