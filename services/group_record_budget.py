from domain import GroupRecordBudget, Group, Record
from services.base_service import BaseService


class GroupRecordBudgetService(BaseService):

    def create(
        self,
        from_group: Group,
        from_record: Record
    ):
        self.repository.create(GroupRecordBudget(
            from_group=from_group,
            from_record=from_record,

            pk_group_record_budget=None,
            fk_group=None,
            fk_record=None
        ))

    def read(self, pk_group_record_budget: int) -> GroupRecordBudget:
        return self.repository.read(
            GroupRecordBudget,
            lambda: GroupRecordBudget.pk_group_record_budget == pk_group_record_budget
        )

    def delete(self):
        ...
