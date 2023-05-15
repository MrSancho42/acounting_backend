from domain import Business, User
from services.base_service import BaseService


class BusinessService(BaseService):

    def create(
        self,
        name: str,
        owner: User,
        pk_business=None,
        fk_user=None
    ):
        self.repository.create(Business(name=name, owner=owner, pk_business=pk_business, fk_user=fk_user))

    def read(self, pk_business: int) -> Business:
        return self.repository.read(Business, lambda: Business.pk_business == pk_business)

    def delete(self):
        ...

    def get_businesses(self, user: User):
        return list(map(
            lambda business: {'pk_business': business.pk_business, 'name': business.name}, user.businesses
        ))
