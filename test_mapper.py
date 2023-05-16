import sqlalchemy.orm

import adapter_orm
import secrets
from domain import RecordKinds
from repository import SqlAlchemyRepository
from services import (
    UserService,
    BusinessService,
    BillService,
    RecordService,
    BusinessRecordService,
    EmployeeService,
    CreditService,
    UserCategoryService,
    BusinessCategoryService,
    BusinessSubCategoryService,
    UserSubCategoryService
)


engine = sqlalchemy.create_engine(
    f'postgresql+psycopg2://{secrets.DB_USER_NAME}:{secrets.DB_USER_PASSWORD}@localhost:5432/accounting_db'
)

# engine = sqlalchemy.create_engine('sqlite:///./db.db')

adapter_orm.metadata.create_all(engine)
adapter_orm.mappers()
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

repository = SqlAlchemyRepository(session)
user_service = UserService(repository)
business_service = BusinessService(repository)
bill_service = BillService(repository)
record_service = RecordService(repository)
business_record_service = BusinessRecordService(repository)
employee_service = EmployeeService(repository)
credit_service = CreditService(repository)
user_category_service = UserCategoryService(repository)
business_category_service = BusinessCategoryService(repository)
user_sub_category_service = UserSubCategoryService(repository)
business_sub_category_service = BusinessSubCategoryService(repository)

# business_sub_category_service.create(
#     from_business=business_service.read(1),
#     from_sub_category=sub_category_service.read(1),
# )

# sub_category_service.create(name='qwerty', depends_on_category=category_service.read(1))

# business_category_service.create(
#     business_service.read(1),
#     category_service.read(1),
# )

# user_category_service.create(
#     user_service.read(1),
#     category_service.read(1),
#     name='fastfood',
#     colour='123456',
#     ico='path'
# )

# category_service.create(name='Food')

# credit_service.create(
#     name='Іпотека',
#     credit_owner=user_service.read(1),
#     total_cost=145,
#     total_size=140,
# )

# business_employee_service.create(
#         fk_business=business_service.read(1).pk_business,
#         fk_employee=employee_service.read(1).pk_employee
# )

# employee_service.create(
#     name='Ok'
# )
# business_record_service.create(
#     from_bill=bill_service.read(1),
#     from_business=business_service.read(1),
#     amount=34.3,
#     description='Business rec',
#     kind=RecordKinds.SPENDING
# )
#business_service.create(name='New Business', owner=user_service.read(1))
# record_service.create(
#     from_bill=bill_service.read(2),
#     amount=23.5,
#     description='Alco',
#     kind=RecordKinds.SPENDING
#     )
#user_service.create({'name': 'abc', 'email': 'abc6@gmsil.com', 'password': 'qwe'})
# bill_service.create(
#     owner=user_service.read(1),
#     name='Кредит',
#     amount=2045.57,
#     is_for_business=False,
#     currency='USD',
#     pk_bill=None,
#     fk_user=None
#     )
#print(bill_service.read(1))
#user = user_service.read(1)
#
#user_service.update(1, {'pk_user': 1, 'name': 'string', 'email': 'xxx', 'password': 'string'})
