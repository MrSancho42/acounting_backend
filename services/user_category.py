from domain import Category, User, UserCategory
from services.base_service import BaseService


class UserCategoryService(BaseService):

    def create(
        self,
        from_user: User,
        from_category: Category,
        pk_user_category: int = None,
        fk_category: int = None,
        fk_user: int = None
    ):
        self.repository.create(UserCategory(
            from_user=from_user,
            from_category=from_category,
            pk_user_category=pk_user_category,
            fk_category=fk_category,
            fk_user=fk_user
        ))

    def read(self, pk_user_category: int) -> UserCategory:
        return self.repository.read(UserCategory, lambda: UserCategory.pk_user_category == pk_user_category)

    def delete(self):
        ...
