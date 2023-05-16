from domain import UserBudgetBySubCategory, User, UserSubCategory
from services.base_service import BaseService


class UserBudgetBySubCategoryService(BaseService):

    def create(
        self,
        name: str,
        limit: float,
        currency: str,

        visibility_to: User,
        from_sub_category: UserSubCategory
    ):
        self.repository.create(UserBudgetBySubCategory(
            name=name,
            limit=limit,
            currency=currency,

            visibility_to=visibility_to,
            from_user_sub_category=from_sub_category,

            pk_user_budget_by_sub_category=None,
            fk_user=None,
            fk_user_sub_category=None
        ))

    def read(self, pk_user_budget_by_sub_category: int) -> UserBudgetBySubCategory:
        return self.repository.read(
            UserBudgetBySubCategory,
            lambda: UserBudgetBySubCategory.pk_user_budget_by_sub_category == pk_user_budget_by_sub_category
        )

    def delete(self):
        ...
