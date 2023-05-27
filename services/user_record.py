from datetime import datetime

from domain import Bill, UserRecord, RecordKinds, User, UserCategory
from services.base_service import BaseService
from services import BillService


class UserRecordService(BaseService):

    def create(
        self,
        from_bill: Bill,
        from_user_category: UserCategory,
        amount: float,
        description: str,
        kind: RecordKinds,
        creation_time: datetime = datetime.now(),
        currency: str = 'UAH'
    ):
        self.repository.create(UserRecord(
            from_bill=from_bill,
            from_user_category=from_user_category,
            amount=amount,
            description=description,
            kind=kind,
            creation_time=creation_time,
            currency=currency,

            pk_record=None,
            fk_bill=None,
            fk_category=None
        ))

        if kind == RecordKinds.SPENDING:
            BillService.update(self, entity=from_bill, new_data={'amount': from_bill.amount - amount})
        elif kind == RecordKinds.INCOME:
            BillService.update(self, entity=from_bill, new_data={'amount': from_bill.amount + amount})
        elif kind == RecordKinds.TRANSFER:
            raise NotImplemented('TRANSFER not implemented yet.')

    def read(self, pk_record: int) -> UserRecord:
        return self.repository.read(UserRecord, lambda: UserRecord.pk_record == pk_record)

    def delete(self):
        ...

    def get_records(self, from_user: User | None, from_bill: Bill | None):
        records = list()

        if from_user:
            # add to records all user records
            user_bills = from_user.bills
            for bill in user_bills:
                records += bill.records
        elif from_bill:
            # add to records only bill records
            records = from_bill.records

        return list(map(
            lambda record: {
                'pk_record': record.pk_record,
                'amount': record.amount,
                'description': record.description,
                'kind': record.kind,
                'creation_time': record.creation_time,
                'currency': record.currency,
                'fk_category': record.fk_category,
                'category_name': None,
            },
            records
        ))
