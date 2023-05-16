from domain import User, Group, GroupPermission, UserGroupPermission
from services.base_service import BaseService


class UserGroupPermissionService(BaseService):

    def create(
        self,
            permission_owner: User,
            permission_to: Group,
            permission_granted: GroupPermission
    ):
        self.repository.create(UserGroupPermission(
            permission_owner=permission_owner,
            permission_to=permission_to,
            permission_granted=permission_granted,

            pk_user_group_permission=None,
            fk_user=None,
            fk_group=None,
            fk_group_permission=None
        ))

    def read(self, pk_user_group_permission: int) -> UserGroupPermission:
        return self.repository.read(
            UserGroupPermission,
            lambda: UserGroupPermission.pk_user_group_permission == pk_user_group_permission
        )

    def delete(self):
        ...
