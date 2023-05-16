from domain import Employee, Business
from services.base_service import BaseService


class EmployeeService(BaseService):

    def create(
        self,
        from_business: Business,
        name: str
    ):
        self.repository.create(Employee(
            from_business=from_business,
            name=name,

            pk_employee=None,
            fk_business=None
        ))

    def read(self, pk_employee: int) -> Employee:
        return self.repository.read(Employee, lambda: Employee.pk_employee == pk_employee)

    def delete(self):
        ...
