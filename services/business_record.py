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
        pk_record: int = None,
        fk_bill: int = None,
        fk_business: int = None
    ):
        self.repository.create(BusinessRecord(
            from_bill=from_bill,
            from_business=from_business,
            amount=amount,
            description=description,
            kind=kind,
            creation_time=creation_time,
            currency=currency,
            pk_record=pk_record,
            fk_bill=fk_bill,
            fk_business=fk_business
        ))

    def read(self, pk_record: int) -> BusinessRecord:
        return self.repository.read(BusinessRecord, lambda: BusinessRecord.pk_record == pk_record)

    def delete(self):
        ...