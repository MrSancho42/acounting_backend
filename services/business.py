from domain import Business, User
from services.base_service import BaseService


class BusinessService(BaseService):

    def create(
        self,
        name: str,
        owner_name: str,
        taxpayer_account_card: str,
        address: str,
        owner: User,
        pk_business=None,
        fk_user=None
    ):
        self.repository.create(Business(
            name=name,
            owner_name=owner_name,
            taxpayer_account_card=taxpayer_account_card,
            address=address,
            owner=owner,
            pk_business=pk_business,
            fk_user=fk_user
        ))

    def read(self, pk_business: int) -> Business:
        return self.repository.read(Business, lambda: Business.pk_business == pk_business)

    def delete(self):
        ...

    def get_businesses(self, user: User):
        return list(map(
            lambda business: {
                'pk_business': business.pk_business,
                'name': business.name,
                'owner_name': business.owner_name,
                'taxpayer_account_card': business.taxpayer_account_card,
                'address': business.address
            }, user.businesses
        ))
