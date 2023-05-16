from domain import Group, User
from services.base_service import BaseService


class GroupService(BaseService):

    def create(
        self,
        name: str,
        owner: User,
        pk_group=None,
        fk_user=None
    ):
        self.repository.create(Group(name=name, owner=owner, pk_group=pk_group, fk_user=fk_user))

    def read(self, pk_group: int) -> Group:
        return self.repository.read(Group, lambda: Group.pk_group == pk_group)

    def delete(self):
        ...
