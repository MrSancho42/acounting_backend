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

    def get_user_categories(self, from_user: User):
        # returns all user categories by user
        user_categories = from_user.user_categories

        return list(map(
            lambda user_category: {
                'pk_user_category': user_category.pk_user_category,
                'name': user_category.name,
                'ico': user_category.ico,
                'colour': user_category.colour,
                'fk_parent_category': user_category.fk_parent_category
            },
            user_categories
        ))
