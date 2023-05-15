from domain import User, Bill

from services.base_service import BaseService


class BillService(BaseService):

    def create(
        self,
        pk_bill: int,
        fk_user: int,
        owner: User,
        name: str,
        amount: float,
        currency: str,
        is_for_business: bool = False
    ):
        self.repository.create(Bill(
            pk_bill=pk_bill,
            fk_user=fk_user,
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
