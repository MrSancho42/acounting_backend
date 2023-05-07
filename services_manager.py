import sqlalchemy

import adapter_orm
from repository import SqlAlchemyRepository
from services import BusinessService, UserService, BillService

engine = sqlalchemy.create_engine('sqlite:///./db.db')


adapter_orm.metadata.create_all(engine)
adapter_orm.mappers()
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

repository = SqlAlchemyRepository(session)

user_service = UserService(repository)
business_service = BusinessService(repository)
bill_service = BillService(repository)
