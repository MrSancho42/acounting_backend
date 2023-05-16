from domain import BusinessSubCategory, BusinessCategory
from services.base_service import BaseService


class BusinessSubCategoryService(BaseService):

    def create(
        self,
        depends_on_business_category: BusinessCategory,
        name: str,
        ico: str,
        colour: str,
    ):
        self.repository.create(BusinessSubCategory(
            depends_on_business_category=depends_on_business_category,
            name=name,
            ico=ico,
            colour=colour,

            pk_business_sub_category=None,
            fk_business_category=None
        ))

    def read(self, pk_business_sub_category: int) -> BusinessSubCategory:
        return self.repository.read(
            BusinessSubCategory,
            lambda: BusinessSubCategory.pk_business_sub_category == pk_business_sub_category
        )

    def delete(self):
        ...
