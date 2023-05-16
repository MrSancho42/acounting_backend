from datetime import datetime

from domain import GroupRecord, Record, Group
from services.base_service import BaseService


class GroupRecordService(BaseService):

    def create(
        self,
        from_group: Group,
        from_record: Record,
    ):
        self.repository.create(GroupRecord(
            from_group=from_group,
            from_record=from_record,

            pk_group_record=None,
            fk_record=None,
            fk_group=None
        ))

    def read(self, pk_record: int) -> GroupRecord:
        return self.repository.read(GroupRecord, lambda: GroupRecord.pk_record == pk_record)

    def delete(self):
        ...
