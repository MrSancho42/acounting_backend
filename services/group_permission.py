from domain import GroupPermission
from services.base_service import BaseService
import uuid


class GroupPermissionService(BaseService):

    def create(self, permission_description):
        self.repository.create(GroupPermission(
            permission_description=permission_description,

            pk_group_permission=None
        ))

    def read(self, pk_group_permission: int) -> GroupPermission:
        return self.repository.read(
            GroupPermission,
            lambda: GroupPermission.pk_group_permission == pk_group_permission
        )

    def delete(self):
        ...
