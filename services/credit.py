from domain import User, Credit
from datetime import datetime
from services.base_service import BaseService


class CreditService(BaseService):

    def create(
        self,
        name: str,
        credit_owner: User,
        total_cost: float,
        total_size: float,
        due_date: datetime = datetime.now(),
        pk_credit=None,
        fk_user=None
    ):
        self.repository.create(Credit(
            name=name,
            credit_owner=credit_owner,
            total_cost=total_cost,
            total_size=total_size,
            due_date=due_date,
            pk_credit=pk_credit,
            fk_user=fk_user
        ))

    def read(self, pk_credit: int) -> Credit:
        return self.repository.read(Credit, lambda: Credit.pk_credit == pk_credit)

    def delete(self):
        ...
