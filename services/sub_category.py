from domain import Category, SubCategory
from services.base_service import BaseService


class SubCategoryService(BaseService):

    def create(
        self,
        name: str,
        depends_on_category: Category,
        pk_sub_category: int = None,
        fk_category: int = None,
        ico: str = None,
        colour: str = None
    ):
        self.repository.create(SubCategory(
            name=name,
            depends_on_category=depends_on_category,
            pk_sub_category=pk_sub_category,
            fk_category=fk_category,
            ico=ico,
            colour=colour
        ))

    def read(self, pk_sub_category: int) -> SubCategory:
        return self.repository.read(
            SubCategory,
            lambda: SubCategory.pk_sub_category == pk_sub_category
        )

    def delete(self):
        ...
