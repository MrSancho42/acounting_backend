from domain import GroupPermissions
from services.base_service import BaseService
import uuid


class GroupPermissionsService(BaseService):

    def create(self, permission_description):
        print(permission_description)
        self.repository.create(GroupPermissions(
            permission_description=permission_description,

            pk_group_permission=None
        ))

    def read(self, pk_group_permission: int) -> GroupPermissions:
        return self.repository.read(
            GroupPermissions,
            lambda: GroupPermissions.pk_group_permission == pk_group_permission
        )

    def delete(self):
        ...
