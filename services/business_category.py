from domain import Business, BusinessCategory
from services.base_service import BaseService


class BusinessCategoryService(BaseService):

    def create(
        self,
        from_business: Business,
        name: str,
        ico: str,
        colour: str,
        from_parent: BusinessCategory | None = None
    ):
        print('business category services')
        self.repository.create(BusinessCategory(
            from_business=from_business,
            from_parent=from_parent,
            name=name,
            ico=ico,
            colour=colour,

            pk_business_category=None,
            fk_business=None,
            fk_parent_category=None
        ))

    def read(self, pk_business_category: int) -> BusinessCategory:
        return self.repository.read(
            BusinessCategory,
            lambda: BusinessCategory.pk_business_category == pk_business_category
        )

    def delete(self):
        ...

    def get_business_categories(self, from_business: Business):
        # returns all business categories by business
        business_categories = from_business.business_categories

        return list(map(
            lambda business_category: {
                'pk_business_category': business_category.pk_business_category,
                'name': business_category.name,
                'ico': business_category.ico,
                'colour': business_category.colour,
                'fk_parent_category': business_category.fk_parent_category
            },
            business_categories
        ))
