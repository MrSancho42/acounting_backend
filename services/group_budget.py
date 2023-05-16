from domain import Group, GroupBudget
from services.base_service import BaseService


class GroupBudgetService(BaseService):

    def create(
        self,
        name: str,
        limit: float,
        currency: str,

        from_group: Group
    ):
        self.repository.create(GroupBudget(
            name=name,
            limit=limit,
            currency=currency,
            from_group=from_group,

            pk_group_budget=None,
            fk_group=None
        ))

    def read(self, pk_group_budget: int) -> GroupBudget:
        return self.repository.read(
            GroupBudget,
            lambda: GroupBudget.pk_group_budget == pk_group_budget
        )

    def delete(self):
        ...
