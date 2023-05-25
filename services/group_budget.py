from domain import Group, GroupBudget, BudgetKinds, GroupCategoryBudget, GroupCategory, GroupRecordBudget
from services.base_service import BaseService


class GroupBudgetService(BaseService):

    def create(
        self,
        name: str,
        limit: float,
        currency: str,
        kind: BudgetKinds,

        from_group: Group,
        from_category: GroupCategory = None
    ):
        new_pk_group_budget = self.repository.create(GroupBudget(
            name=name,
            limit=limit,
            currency=currency,
            kind=kind,
            from_group=from_group,

            pk_group_budget=None,
            fk_group=None
        ))

        if kind == BudgetKinds.BY_RECORD:
            ...
        elif kind == BudgetKinds.BY_CATEGORY and from_category:
            self.repository.create(GroupCategoryBudget(
                from_group_budget=new_pk_group_budget,
                from_group_category=from_category,

                pk_group_category_budget=None,
                fk_group_budget=None,
                fk_group_category=None
            ))

    def read(self, pk_group_budget: int) -> GroupBudget:
        return self.repository.read(
            GroupBudget,
            lambda: GroupBudget.pk_group_budget == pk_group_budget
        )


    def get_category_id(self, pk_group_budget: int):
        category_budget = self.repository.read(
            GroupCategoryBudget,
            lambda: GroupCategoryBudget.fk_group_budget == pk_group_budget
        )
        return category_budget.fk_group_category

    def get_group_budget_categories(self, from_group: Group):
        group_budgets = from_group.group_budgets
        group_budget_categories = list()
        for budget in group_budgets:
            if budget.kind == BudgetKinds.BY_CATEGORY:
                group_budget_categories.append(budget)

        return list(map(
            lambda group_budget_category: {
                'pk_group_budget': group_budget_category.pk_group_budget,
                'name': group_budget_category.name,
                'limit': group_budget_category.limit,
                'currency': group_budget_category.currency,
                'kind': group_budget_category.kind,
                'fk_group_category': self.get_category_id(group_budget_category.pk_group_budget)
            },
            group_budget_categories
        ))

    def get_group_budget_records(self, from_group: Group):
        group_budgets = from_group.group_budgets
        group_budget_categories = list()
        for budget in group_budgets:
            if budget.kind == BudgetKinds.BY_RECORD:
                group_budget_categories.append(budget)

        return list(map(
            lambda group_budget_category: {
                'pk_group_budget': group_budget_category.pk_group_budget,
                'name': group_budget_category.name,
                'limit': group_budget_category.limit,
                'currency': group_budget_category.currency,
                'kind': group_budget_category.kind
            },
            group_budget_categories
        ))

    def delete(self):
        ...
