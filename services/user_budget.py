from domain import User, UserBudget, BudgetKinds, UserCategoryBudget, UserCategory, UserRecordBudget
from services.base_service import BaseService


class UserBudgetService(BaseService):
    new_user_budget: UserBudget

    def create(
        self,
        name: str,
        limit: float,
        currency: str,
        kind: BudgetKinds,

        from_user: User,
        from_category: UserCategory = None
    ):
        self.new_user_budget = self.repository.create(UserBudget(
            name=name,
            limit=limit,
            currency=currency,
            kind=kind,
            from_user=from_user,

            pk_user_budget=None,
            fk_user=None
        ))

        if kind == BudgetKinds.BY_RECORD:
            ...
        elif kind == BudgetKinds.BY_CATEGORY and from_category:
            self.repository.create(UserCategoryBudget(
                from_user_budget=self.new_user_budget,
                from_user_category=from_category,

                pk_user_category_budget=None,
                fk_user_budget=None,
                fk_user_category=None
            ))

    def read(self, pk_user_budget: int) -> UserBudget:
        return self.repository.read(
            UserBudget,
            lambda: UserBudget.pk_user_budget == pk_user_budget
        )

    def get_category_id(self, pk_user_budget: int):
        category_budget = self.repository.read(
            UserCategoryBudget,
            lambda: UserCategoryBudget.fk_user_budget == pk_user_budget
        )
        return category_budget.fk_user_category

    def get_user_budget_categories(self, from_user: User):
        user_budgets = from_user.user_budgets
        user_budget_categories = list()
        for budget in user_budgets:
            if budget.kind == BudgetKinds.BY_CATEGORY:
                user_budget_categories.append(budget)

        return list(map(
            lambda user_budget_category: {
                'pk_user_budget': user_budget_category.pk_user_budget,
                'name': user_budget_category.name,
                'limit': user_budget_category.limit,
                'currency': user_budget_category.currency,
                'kind': user_budget_category.kind,
                'fk_user_category': self.get_category_id(user_budget_category.pk_user_budget)
            },
            user_budget_categories
        ))

    def get_user_budget_records(self, from_user: User):
        user_budgets = from_user.user_budgets
        user_budget_categories = list()
        for budget in user_budgets:
            if budget.kind == BudgetKinds.BY_RECORD:
                user_budget_categories.append(budget)

        return list(map(
            lambda user_budget_category: {
                'pk_user_budget': user_budget_category.pk_user_budget,
                'name': user_budget_category.name,
                'limit': user_budget_category.limit,
                'currency': user_budget_category.currency,
                'kind': user_budget_category.kind
            },
            user_budget_categories
        ))

    def delete(self):
        ...
