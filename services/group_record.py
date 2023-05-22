from datetime import datetime

from domain import GroupRecord, Record, Group, Bill, RecordKinds, GroupCategory
from services.base_service import BaseService


class GroupRecordService(BaseService):

    def create(
        self,
        from_bill: Bill,
        from_group: Group,
        from_group_category: GroupCategory,
        amount: float,
        description: str,
        kind: RecordKinds,
        creation_time: datetime = datetime.now(),
        currency: str = 'UAH',
    ):
        self.repository.create(GroupRecord(
            from_bill=from_bill,
            from_group=from_group,
            from_group_category=from_group_category,
            amount=amount,
            description=description,
            kind=kind,
            creation_time=creation_time,
            currency=currency,

            pk_record=None,
            fk_bill=None,
            fk_group=None,
            fk_category=None
        ))

    def read(self, pk_record: int) -> GroupRecord:
        return self.repository.read(GroupRecord, lambda: GroupRecord.pk_record == pk_record)

    def delete(self):
        ...

    def get_group_records(self, from_group: Group, from_bill: Bill | None = None):
        records = list(filter(lambda record: not from_bill or record.from_bill == from_bill, from_group.records))
        return list(map(
            lambda record: {
                'pk_record': record.pk_record,
                'amount': record.amount,
                'description': record.description,
                'kind': record.kind,
                'creation_time': record.creation_time,
                'currency': record.currency,
            },
            records
        ))
