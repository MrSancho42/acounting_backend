from domain import Category, Business, BusinessCategory
from services.base_service import BaseService


class BusinessCategoryService(BaseService):

    def create(
        self,
        from_business: Business,
        from_category: Category,
        pk_user_category: int = None,
        fk_category: int = None,
        fk_user: int = None
    ):
        self.repository.create(BusinessCategory(
            from_business=from_business,
            from_category=from_category,
            pk_business_category=pk_user_category,
            fk_category=fk_category,
            fk_business=fk_user
        ))

    def read(self, pk_business_category: int) -> BusinessCategory:
        return self.repository.read(
            BusinessCategory,
            lambda: BusinessCategory.pk_business_category == pk_business_category
        )

    def delete(self):
        ...
