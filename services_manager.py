import sqlalchemy
from sqlalchemy import orm

import adapter_orm
import secrets
from repository import SqlAlchemyRepository
from services import (
    BillService, BusinessRecordService, BusinessService, UserService, UserRecordService, UserCategoryService,
    BusinessCategoryService, GroupService, GroupCategoryService, GroupRecordService, UserBudgetService,
    GroupBudgetService
)

engine = sqlalchemy.create_engine(
    f'postgresql+psycopg2://{secrets.DB_USER_NAME}:{secrets.DB_USER_PASSWORD}@'
    f'{secrets.DB_ADDRESS}:{secrets.DB_PORT}/{secrets.DB_NAME}'
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
business_category_service = BusinessCategoryService(repository)
user_record_service = UserRecordService(repository)
user_category_service = UserCategoryService(repository)
group_service = GroupService(repository)
group_category_service = GroupCategoryService(repository)
group_record_service = GroupRecordService(repository)
user_category_budget_service = UserBudgetService(repository)
user_budget_service = UserBudgetService(repository)
group_budget_service = GroupBudgetService(repository)
