from domain import User, Credit
from datetime import datetime
from services.base_service import BaseService


class CreditService(BaseService):

    def create(
        self,
        owner: User,
        name: str,
        total_cost: float,
        total_size: float,
        due_date: datetime = datetime.now()
    ):
        self.repository.create(Credit(
            owner=owner,
            name=name,
            total_cost=total_cost,
            total_size=total_size,
            due_date=due_date,

            pk_credit=None,
            fk_user=None
        ))

    def read(self, pk_credit: int) -> Credit:
        return self.repository.read(Credit, lambda: Credit.pk_credit == pk_credit)

    def delete(self):
        ...
