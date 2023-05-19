from datetime import datetime

from domain import Bill, BusinessRecord, RecordKinds, Business
from services.base_service import BaseService


class BusinessRecordService(BaseService):

    def create(
        self,
        from_bill: Bill,
        from_business: Business,
        amount: float,
        description: str,
        kind: RecordKinds,
        creation_time: datetime = datetime.now(),
        currency: str = 'UAH',
    ):
        self.repository.create(BusinessRecord(
            from_bill=from_bill,
            from_business=from_business,
            amount=amount,
            description=description,
            kind=kind,
            creation_time=creation_time,
            currency=currency,

            pk_record=None,
            fk_bill=None,
            fk_business=None,
        ))

    def read(self, pk_record: int) -> BusinessRecord:
        return self.repository.read(BusinessRecord, lambda: BusinessRecord.pk_record == pk_record)

    def delete(self):
        ...

    def get_business_records(self, from_business: Business, from_bill: Bill | None = None):
        records = list(filter(lambda record: not from_bill or record.from_bill == from_bill, from_business.records))
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
