from domain import Category
from services.base_service import BaseService


class CategoryService(BaseService):

    def create(
        self,
        name: str,
        pk_category: int = None,
        ico: str = None,
        colour: str = None
    ):
        self.repository.create(Category(pk_category=pk_category, name=name, ico=ico, colour=colour))

    def read(self, pk_category: int) -> Category:
        return self.repository.read(Category, lambda: Category.pk_category == pk_category)

    def delete(self):
        ...
