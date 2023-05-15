from domain import SubCategory, Business, BusinessSubCategory
from services.base_service import BaseService


class BusinessSubCategoryService(BaseService):

    def create(
        self,
        from_business: Business,
        from_sub_category: SubCategory,
        pk_business_sub_category: int = None,
        fk_sub_category: int = None,
        fk_business: int = None
    ):
        self.repository.create(BusinessSubCategory(
            from_business=from_business,
            from_sub_category=from_sub_category,
            pk_business_sub_category=pk_business_sub_category,
            fk_sub_category=fk_sub_category,
            fk_business=fk_business
        ))

    def read(self, pk_business_sub_category: int) -> BusinessSubCategory:
        return self.repository.read(
            BusinessSubCategory,
            lambda: BusinessSubCategory.pk_business_sub_category == pk_business_sub_category
        )

    def delete(self):
        ...
