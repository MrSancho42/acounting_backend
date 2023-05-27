from datetime import datetime

from domain import Bill, BusinessRecord, RecordKinds, Business, BusinessCategory, RecordSubKinds
from services.base_service import BaseService
from services import BillService


class BusinessRecordService(BaseService):

    def create(
        self,
        from_bill: Bill,
        from_business: Business,
        from_business_category: BusinessCategory,
        amount: float,
        description: str,
        kind: RecordKinds,
        sub_kind: RecordSubKinds,
        creation_time: datetime = datetime.now(),
        currency: str = 'UAH',
    ):
        self.repository.create(BusinessRecord(
            from_bill=from_bill,
            from_business=from_business,
            from_business_category=from_business_category,
            amount=amount,
            description=description,
            kind=kind,
            sub_kind=sub_kind,
            creation_time=creation_time,
            currency=currency,

            pk_record=None,
            fk_bill=None,
            fk_business=None,
            fk_category=None
        ))

        if kind == RecordKinds.SPENDING:
            BillService.update(self, entity=from_bill, new_data={'amount': from_bill.amount - amount})
        elif kind == RecordKinds.INCOME:
            BillService.update(self, entity=from_bill, new_data={'amount': from_bill.amount + amount})
        elif kind == RecordKinds.TRANSFER:
            raise NotImplemented('TRANSFER not implemented yet.')

    def read(self, pk_record: int) -> BusinessRecord:
        return self.repository.read(BusinessRecord, lambda: BusinessRecord.pk_record == pk_record)

    def delete(self):
        ...

    def sort_by_date(self, record: BusinessRecord):
        return record.creation_time.timestamp()

    def get_business_records(self, from_business: Business, from_bill: Bill | None = None):
        records = sorted(from_business.records, key=self.sort_by_date, reverse=True)
        records = list(filter(lambda record: from_bill is None or record.from_bill == from_bill, records))
        return list(map(
            lambda record: {
                'pk_record': record.pk_record,
                'fk_bill': record.fk_bill,
                'amount': record.amount,
                'description': record.description,
                'kind': record.kind,
                'sub_kind': record.sub_kind,
                'creation_time': record.creation_time,
                'currency': record.currency,
            },
            records
        ))
