from domain import User, Business, UserException
from sqlalchemy import exc


class SqlAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def apply_changes(self):
        self.session.commit()

    def create(self, entity):
        try:
            self.session.add(entity)
            self.session.commit()
            return entity
        except exc.IntegrityError:
            self.session.rollback()
            raise UserException.MailAlreadyInUse

    def read(self, domain, criteria):
        try:
            return self.session.query(domain).filter(criteria).one()
        except exc.NoResultFound:
            raise UserException.UserNotFound

    def delete(self): ...
