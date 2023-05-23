from domain import Group, GroupCategory
from services.base_service import BaseService


class GroupCategoryService(BaseService):

    def create(
        self,
        from_group: Group,
        name: str,
        ico: str,
        colour: str,
        from_parent: GroupCategory | None = None
    ):
        self.repository.create(GroupCategory(
            from_group=from_group,
            from_parent=from_parent,
            name=name,
            ico=ico,
            colour=colour,

            pk_group_category=None,
            fk_group=None,
            fk_parent_category=None
        ))

    def read(self, pk_group_category: int) -> GroupCategory:
        return self.repository.read(
            GroupCategory,
            lambda: GroupCategory.pk_group_category == pk_group_category
        )

    def delete(self):
        ...

    def get_group_categories(self, from_group: Group):
        # returns all group categories by group
        group_categories = from_group.group_categories

        return list(map(
            lambda group_category: {
                'pk_group_category': group_category.pk_group_category,
                'name': group_category.name,
                'ico': group_category.ico,
                'colour': group_category.colour,
                'fk_parent_category': group_category.fk_parent_category
            },
            group_categories
        ))
