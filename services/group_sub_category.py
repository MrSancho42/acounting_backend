from domain import GroupSubCategory, GroupCategory
from services.base_service import BaseService


class GroupSubCategoryService(BaseService):

    def create(
        self,
        depends_on_group_category: GroupCategory,
        name: str,
        ico: str,
        colour: str,
    ):
        self.repository.create(GroupSubCategory(
            depends_on_group_category=depends_on_group_category,
            name=name,
            ico=ico,
            colour=colour,

            pk_group_sub_category=None,
            fk_group_category=None
        ))

    def read(self, pk_group_sub_category: int) -> GroupSubCategory:
        return self.repository.read(
            GroupSubCategory,
            lambda: GroupSubCategory.pk_group_sub_category == pk_group_sub_category
        )

    def delete(self):
        ...
