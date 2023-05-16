from domain import UserBudgetByCategory, User, UserCategory
from services.base_service import BaseService


class UserBudgetByCategoryService(BaseService):

    def create(
        self,
        name: str,
        limit: float,
        currency: str,

        visibility_to: User,
        from_user_category: UserCategory
    ):
        self.repository.create(UserBudgetByCategory(
            name=name,
            limit=limit,
            currency=currency,

            visibility_to=visibility_to,
            from_user_category=from_user_category,

            pk_user_budget_by_category=None,
            fk_user=None,
            fk_user_category=None
        ))

    def read(self, pk_user_budget_by_category: int) -> UserBudgetByCategory:
        return self.repository.read(
            UserBudgetByCategory,
            lambda: UserBudgetByCategory.pk_user_budget_by_category == pk_user_budget_by_category
        )

    def delete(self):
        ...
