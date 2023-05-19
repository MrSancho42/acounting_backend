import sqlalchemy

import adapter_orm
import secrets
from repository import SqlAlchemyRepository
from services import (
    BillService, BusinessRecordService, BusinessService, UserService
)

engine = sqlalchemy.create_engine(
    f'postgresql+psycopg2://{secrets.DB_USER_NAME}:{secrets.DB_USER_PASSWORD}@localhost:5432/accounting_db'
)

adapter_orm.metadata.create_all(engine)
adapter_orm.mappers()

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

repository = SqlAlchemyRepository(session)

user_service = UserService(repository)
business_service = BusinessService(repository)
bill_service = BillService(repository)
business_record_service = BusinessRecordService(repository)
