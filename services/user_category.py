from domain import User, UserCategory
from services.base_service import BaseService


class UserCategoryService(BaseService):

    def create(
        self,
        from_user: User,
        name: str,
        ico: str,
        colour: str,
        from_parent: UserCategory | None = None
    ):
        self.repository.create(UserCategory(
            from_user=from_user,
            from_parent=from_parent,
            name=name,
            ico=ico,
            colour=colour,

            pk_user_category=None,
            fk_user=None,
            fk_parent_category=None
        ))

    def read(self, pk_user_category: int) -> UserCategory:
        return self.repository.read(UserCategory, lambda: UserCategory.pk_user_category == pk_user_category)

    def delete(self):
        ...
