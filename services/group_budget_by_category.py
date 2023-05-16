from domain import GroupBudgetByCategory, Group, GroupCategory
from services.base_service import BaseService


class GroupBudgetByCategoryService(BaseService):

    def create(
        self,
        name: str,
        limit: float,
        currency: str,

        visibility_to: Group,
        from_group_category: GroupCategory
    ):
        self.repository.create(GroupBudgetByCategory(
            name=name,
            limit=limit,
            currency=currency,

            visibility_to=visibility_to,
            from_group_category=from_group_category,

            pk_group_budget_by_category=None,
            fk_group=None,
            fk_group_category=None
        ))

    def read(self, pk_group_budget_by_category: int) -> GroupBudgetByCategory:
        return self.repository.read(
            GroupBudgetByCategory,
            lambda: GroupBudgetByCategory.pk_group_budget_by_category == pk_group_budget_by_category
        )

    def delete(self):
        ...
