from domain import User, UserBudget
from services.base_service import BaseService


class UserBudgetService(BaseService):

    def create(
        self,
        name: str,
        limit: float,
        currency: str,

        from_user: User
    ):
        self.repository.create(UserBudget(
            name=name,
            limit=limit,
            currency=currency,
            from_user=from_user,

            pk_user_budget=None,
            fk_user=None
        ))

    def read(self, pk_user_budget: int) -> UserBudget:
        return self.repository.read(
            UserBudget,
            lambda: UserBudget.pk_user_budget == pk_user_budget
        )

    def delete(self):
        ...
