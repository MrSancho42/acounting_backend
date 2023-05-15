from datetime import datetime

from domain import Bill, Record, RecordKinds
from services.base_service import BaseService


class RecordService(BaseService):

    def create(
        self,
        from_bill: Bill,
        amount: float,
        description: str,
        kind: RecordKinds,
        creation_time: datetime = datetime.now(),
        currency: str = 'UAH',
        pk_record=None,
        fk_bill=None
    ):
        self.repository.create(Record(
            pk_record=pk_record,
            fk_bill=fk_bill,
            from_bill=from_bill,
            amount=amount,
            description=description,
            kind=kind,
            creation_time=creation_time,
            currency=currency
        ))

    def read(self, pk_record: int) -> Record:
        return self.repository.read(Record, lambda: Record.pk_record == pk_record)

    def delete(self):
        ...
