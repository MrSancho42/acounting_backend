from domain import SubCategory, User, UserSubCategory
from services.base_service import BaseService


class UserSubCategoryService(BaseService):

    def create(
        self,
        from_user: User,
        from_sub_category: SubCategory,
        pk_user_sub_category: int = None,
        fk_sub_category: int = None,
        fk_user: int = None
    ):
        self.repository.create(UserSubCategory(
            from_user=from_user,
            from_sub_category=from_sub_category,
            pk_user_sub_category=pk_user_sub_category,
            fk_sub_category=fk_sub_category,
            fk_user=fk_user
        ))

    def read(self, pk_user_sub_category: int) -> UserSubCategory:
        return self.repository.read(
            UserSubCategory,
            lambda: UserSubCategory.pk_user_sub_category == pk_user_sub_category
        )

    def delete(self):
        ...
