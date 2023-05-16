from domain import UserRecordBudget, User, Record
from services.base_service import BaseService


class UserRecordBudgetService(BaseService):

    def create(
        self,
        from_user: User,
        from_record: Record
    ):
        self.repository.create(UserRecordBudget(
            from_user=from_user,
            from_record=from_record,

            pk_user_record_budget=None,
            fk_user=None,
            fk_record=None
        ))

    def read(self, pk_user_record_budget: int) -> UserRecordBudget:
        return self.repository.read(
            UserRecordBudget,
            lambda: UserRecordBudget.pk_user_record_budget == pk_user_record_budget
        )

    def delete(self):
        ...
