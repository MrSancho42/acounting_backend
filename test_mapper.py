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
    GroupPermissionService,
    GroupService,
    UserGroupPermissionService,
    GroupRecordService,
    GroupCategoryService,
    UserBudgetByCategoryService,
    GroupBudgetByCategoryService,
    UserBudgetService,
    GroupBudgetService,
    UserRecordBudgetService,
    GroupRecordBudgetService
)


engine = sqlalchemy.create_engine(
    f'postgresql+psycopg2://{secrets.DB_USER_NAME}:{secrets.DB_USER_PASSWORD}@localhost:5432/accounting_db'
)
# engine = sqlalchemy.create_engine('sqlite:///./db.db')


adapter_orm.metadata.drop_all(engine)
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
group_permission_service = GroupPermissionService(repository)
group_service = GroupService(repository)
user_group_permission_service = UserGroupPermissionService(repository)
group_record_service = GroupRecordService(repository)
group_category_service = GroupCategoryService(repository)
user_budget_by_category_service = UserBudgetByCategoryService(repository)
group_budget_by_category_service = GroupBudgetByCategoryService(repository)
user_budget_service = UserBudgetService(repository)
group_budget_service = GroupBudgetService(repository)
user_record_budget_service = UserRecordBudgetService(repository)
group_record_budget_service = GroupRecordBudgetService(repository)

########################################################################################################################
# create users
user_service.create({'name': 'Софія Ткачук', 'email': 'sofiia@gmail.com', 'password': 'qwerty'})
user_service.create({'name': 'Олександр Возний', 'email': 'sasha@gmail.com', 'password': '123456'})

########################################################################################################################
# create user categories
user_category_service.create(
    from_user=user_service.read(1), name='Їжа', ico='/ico', colour='FFFFFF'
)
user_category_service.create(
    from_user=user_service.read(1), name='Надходження', ico='/ico', colour='FFFFFF'
)
user_category_service.create(
    from_user=user_service.read(1), name='Розваги', ico='/ico', colour='FFFFFF'
)
user_category_service.create(
    from_user=user_service.read(1),
    name='Фастфуд', ico='/ico',
    colour='FFFFFF',
    from_parent=user_category_service.read(1)
)
user_category_service.create(
    from_user=user_service.read(1),
    name='Продовольчі товари',
    ico='/ico',
    colour='FFFFFF',
    from_parent=user_category_service.read(1)
)
#################################
user_category_service.create(
    from_user=user_service.read(2), name='Їжа', ico='/ico', colour='FFFFFF'
)
user_category_service.create(
    from_user=user_service.read(2), name='Надходження', ico='/ico', colour='FFFFFF'
)
user_category_service.create(
    from_user=user_service.read(2), name='Розваги', ico='/ico', colour='FFFFFF'
)
user_category_service.create(
    from_user=user_service.read(2),
    name='Фастфуд', ico='/ico',
    colour='FFFFFF',
    from_parent=user_category_service.read(6)
)
user_category_service.create(
    from_user=user_service.read(2),
    name='Продовольчі товари',
    ico='/ico',
    colour='FFFFFF',
    from_parent=user_category_service.read(6)
)

########################################################################################################################
# create bills
bill_service.create(
    owner=user_service.read(1), name='Приватбанк', amount=1000, currency='UAH', is_for_business=False
)
bill_service.create(
    owner=user_service.read(1), name='УкрСиб', amount=20000, currency='UAH', is_for_business=False
)
#################################
bill_service.create(
    owner=user_service.read(2), name='Приват', amount=5000, currency='UAH', is_for_business=False
)
bill_service.create(
    owner=user_service.read(2), name='МоноБанк', amount=500, currency='UAH', is_for_business=False
)

########################################################################################################################
# create records
record_service.create(
    from_bill=bill_service.read(1), amount=140, description='Книга', kind=RecordKinds.SPENDING, currency='UAH'
)
record_service.create(
    from_bill=bill_service.read(1), amount=550.5, description='Концерт', kind=RecordKinds.SPENDING, currency='UAH'
)
record_service.create(
    from_bill=bill_service.read(1), amount=1980, description='Стипендія', kind=RecordKinds.INCOME, currency='UAH'
)
record_service.create(
    from_bill=bill_service.read(2), amount=18000, description='ЗП', kind=RecordKinds.INCOME, currency='UAH'
)
#################################
record_service.create(
    from_bill=bill_service.read(3), amount=210, description='Пузата', kind=RecordKinds.SPENDING, currency='UAH'
)
record_service.create(
    from_bill=bill_service.read(3), amount=5.5, description='Вода', kind=RecordKinds.SPENDING, currency='UAH'
)
record_service.create(
    from_bill=bill_service.read(3), amount=1980, description='Стипендія', kind=RecordKinds.INCOME, currency='UAH'
)
record_service.create(
    from_bill=bill_service.read(3), amount=23500, description='ЗП', kind=RecordKinds.INCOME, currency='UAH'
)

########################################################################################################################
# create businesses

business_service.create(
    name='кав\'ярня',
    owner=user_service.read(2)
)

########################################################################################################################
# create business categories
business_category_service.create(
    from_business=business_service.read(1),
    name='Витрати на закупівлі',
    ico='/ico',
    colour='FFFFFF'
)
business_category_service.create(
    from_business=business_service.read(1),
    name='Закупівля обладнання',
    ico='/ico',
    colour='FFFFFF',
    from_parent=business_category_service.read(1)
)
business_category_service.create(
    from_business=business_service.read(1),
    name='Закупівля розхідних матеріалів',
    ico='/ico',
    colour='FFFFFF',
    from_parent=business_category_service.read(1)
)

########################################################################################################################
# create business records
business_record_service.create(
    from_bill=bill_service.read(3),
    from_business=business_service.read(1),
    amount=1000,
    description='Покупка кавоварок',
    kind=RecordKinds.SPENDING,
    currency='UAH'
)

########################################################################################################################
# create groups
group_service.create(name='сім\'я', owner=user_service.read(1))

########################################################################################################################
# create group categories
group_category_service.create(from_group=group_service.read(1), name='Сімейний відпочинок', ico='/ico', colour='FFFFFF')
group_category_service.create(
    from_group=group_service.read(1),
    name='Кіно',
    ico='/ico',
    colour='FFFFFF',
    from_parent=group_category_service.read(1)
)
group_category_service.create(
    from_group=group_service.read(1),
    name='Ресторани',
    ico='/ico',
    colour='FFFFFF',
    from_parent=group_category_service.read(1)
)
