from domain import User, UserException
from services.base_service import BaseService


class UserService(BaseService):

    def create(self, user_data: dict):
        user_data['pk_user'] = None
        self.repository.create(User(**user_data))

    def read(self, pk_user: int) -> User:
        return self.repository.read(User, lambda: User.pk_user == pk_user)

    def find_user_by_email(self, email: str) -> User:
        return self.repository.read(User, lambda: User.email == email)

    def update(self, pk_user: int, new_data: dict):
        email = new_data.get('email')
        try:
            if email and self.repository.read(User, lambda: User.email == email):
                raise UserException.MailAlreadyInUse
        except UserException.UserNotFound:
            super().update(self.read(pk_user), new_data)

    def delete(self): ...
