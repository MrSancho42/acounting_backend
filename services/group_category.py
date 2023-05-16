from domain import Group, GroupCategory
from services.base_service import BaseService


class GroupCategoryService(BaseService):

    def create(
        self,
        from_group: Group,
        name: str,
        ico: str,
        colour: str,
    ):
        self.repository.create(GroupCategory(
            name=name,
            ico=ico,
            colour=colour,
            from_group=from_group,

            pk_group_category=None,
            fk_group=None
        ))

    def read(self, pk_group_category: int) -> GroupCategory:
        return self.repository.read(
            GroupCategory,
            lambda: GroupCategory.pk_group_category == pk_group_category
        )

    def delete(self):
        ...
