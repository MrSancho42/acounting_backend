from domain import Business, BusinessCategory
from services.base_service import BaseService


class BusinessCategoryService(BaseService):

    def create(
        self,
        from_business: Business,
        name: str,
        ico: str,
        colour: str,
    ):
        self.repository.create(BusinessCategory(
            name=name,
            ico=ico,
            colour=colour,
            from_business=from_business,

            pk_business_category=None,
            fk_business=None
        ))

    def read(self, pk_business_category: int) -> BusinessCategory:
        return self.repository.read(
            BusinessCategory,
            lambda: BusinessCategory.pk_business_category == pk_business_category
        )

    def delete(self):
        ...
