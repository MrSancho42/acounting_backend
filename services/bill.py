from domain import User, Bill

from services.base_service import BaseService


class BillService(BaseService):

    def create(
        self,
        owner: User,
        name: str,
        amount: float,
        currency: str,
        is_for_business: bool = False
    ):
        self.repository.create(Bill(
            pk_bill=None,
            fk_user=None,
            owner=owner,
            name=name,
            amount=amount,
            currency=currency,
            is_for_business=is_for_business
        ))

    def read(self, pk_bill: int) -> Bill:
        return self.repository.read(Bill, lambda: Bill.pk_bill == pk_bill)

    def delete(self):
        ...

    def get_bills(self, user: User):
        return list(map(
            lambda bill: {
                'pk_bill': bill.pk_bill,
                'name': bill.name,
                'amount': bill.amount,
                'currency': bill.currency,
                'is_for_business': bill.is_for_business
            },
            user.bills
        ))
