from domain import User, UserCategory
from services.base_service import BaseService


class UserCategoryService(BaseService):

    def create(
        self,
        from_user: User,
        name: str,
        ico: str,
        colour: str
    ):
        self.repository.create(UserCategory(
            from_user=from_user,
            name=name,
            ico=ico,
            colour=colour,

            pk_user_category=None,
            fk_user=None
        ))

    def read(self, pk_user_category: int) -> UserCategory:
        return self.repository.read(UserCategory, lambda: UserCategory.pk_user_category == pk_user_category)

    def delete(self):
        ...
