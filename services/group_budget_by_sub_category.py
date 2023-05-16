from domain import GroupBudgetBySubCategory, Group, GroupSubCategory
from services.base_service import BaseService


class GroupBudgetBySubCategoryService(BaseService):

    def create(
        self,
        name: str,
        limit: float,
        currency: str,

        visibility_to: Group,
        from_group_sub_category: GroupSubCategory
    ):
        self.repository.create(GroupBudgetBySubCategory(
            name=name,
            limit=limit,
            currency=currency,

            visibility_to=visibility_to,
            from_group_sub_category=from_group_sub_category,

            pk_group_budget_by_sub_category=None,
            fk_group=None,
            fk_group_sub_category=None
        ))

    def read(self, pk_group_budget_by_sub_category: int) -> GroupBudgetBySubCategory:
        return self.repository.read(
            GroupBudgetBySubCategory,
            lambda: GroupBudgetBySubCategory.pk_group_budget_by_sub_category == pk_group_budget_by_sub_category
        )

    def delete(self):
        ...
