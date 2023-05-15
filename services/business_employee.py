from domain import BusinessEmployee
from services.base_service import BaseService


class BusinessEmployeeService(BaseService):

    def create(
        self,
        pk_id: int = None,
        fk_business: int = None,
        fk_employee: int = None
    ):
        self.repository.create(BusinessEmployee(
            pk_id=pk_id,
            fk_business=fk_business,
            fk_employee=fk_employee
        ))

    def read(self):
        ...

    def delete(self):
        ...
