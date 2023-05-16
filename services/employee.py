from domain import Employee
from services.base_service import BaseService


class EmployeeService(BaseService):

    def create(
        self,
        name: str,
        pk_employee=None
    ):
        self.repository.create(Employee(name=name, pk_employee=pk_employee))

    def read(self, pk_employee: int) -> Employee:
        return self.repository.read(Employee, lambda: Employee.pk_employee == pk_employee)

    def delete(self):
        ...
