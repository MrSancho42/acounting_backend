from domain import UserCategory, UserSubCategory
from services.base_service import BaseService


class UserSubCategoryService(BaseService):

    def create(
        self,
        depends_on_user_category: UserCategory,
        name: str,
        ico: str,
        colour: str
    ):
        self.repository.create(UserSubCategory(
            depends_on_user_category=depends_on_user_category,
            name=name,
            ico=ico,
            colour=colour,

            pk_user_sub_category=None,
            fk_user_category=None
        ))

    def read(self, pk_user_sub_category: int) -> UserSubCategory:
        return self.repository.read(
            UserSubCategory,
            lambda: UserSubCategory.pk_user_sub_category == pk_user_sub_category
        )

    def delete(self):
        ...
