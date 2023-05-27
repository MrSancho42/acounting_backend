import sqlalchemy.orm

import adapter_orm
import secrets
from domain import RecordKinds, BudgetKinds, RecordSubKinds
from repository import SqlAlchemyRepository
from services import (
    UserService,
    BusinessService,
    BillService,
    UserRecordService,
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
    UserBudgetService,
    GroupBudgetService
)


engine = sqlalchemy.create_engine(
    f'postgresql+psycopg2://{secrets.DB_USER_NAME}:{secrets.DB_USER_PASSWORD}@localhost:5434/accounting_db'
)


adapter_orm.metadata.drop_all(engine)
adapter_orm.metadata.create_all(engine)
adapter_orm.mappers()
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

repository = SqlAlchemyRepository(session)
user_service = UserService(repository)
business_service = BusinessService(repository)
bill_service = BillService(repository)
user_record_service = UserRecordService(repository)
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
user_budget_service = UserBudgetService(repository)
group_budget_service = GroupBudgetService(repository)

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
    name='Фастфуд',
    ico='/ico',
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
    owner=user_service.read(2), name='Картка ФОП', amount=500, currency='UAH', is_for_business=True
)

########################################################################################################################
# create records
user_record_service.create(
    from_bill=bill_service.read(1),
    from_user_category=user_category_service.read(3),
    amount=140,
    description='Книга',
    kind=RecordKinds.SPENDING,
    currency='UAH'
)
user_record_service.create(
    from_bill=bill_service.read(1),
    from_user_category=user_category_service.read(3),
    amount=550.5,
    description='Концерт',
    kind=RecordKinds.SPENDING,
    currency='UAH'
)
user_record_service.create(
    from_bill=bill_service.read(1),
    from_user_category=user_category_service.read(3),
    amount=1980,
    description='Стипендія',
    kind=RecordKinds.INCOME,
    currency='UAH'
)
user_record_service.create(
    from_bill=bill_service.read(2),
    from_user_category=user_category_service.read(3),
    amount=18000,
    description='ЗП',
    kind=RecordKinds.INCOME,
    currency='UAH'
)
#################################
user_record_service.create(
    from_bill=bill_service.read(3),
    from_user_category=user_category_service.read(9),
    amount=210,
    description='Пузата',
    kind=RecordKinds.SPENDING,
    currency='UAH'
)
user_record_service.create(
    from_bill=bill_service.read(3),
    from_user_category=user_category_service.read(9),
    amount=5.5,
    description='Вода',
    kind=RecordKinds.SPENDING,
    currency='UAH'
)
user_record_service.create(
    from_bill=bill_service.read(3),
    from_user_category=user_category_service.read(9),
    amount=1980,
    description='Стипендія',
    kind=RecordKinds.INCOME,
    currency='UAH'
)
user_record_service.create(
    from_bill=bill_service.read(3),
    from_user_category=user_category_service.read(9),
    amount=23500,
    description='ЗП',
    kind=RecordKinds.INCOME,
    currency='UAH'
)

########################################################################################################################
# create businesses

business_service.create(
    name='Кавʼярня',
    owner_name='Кравченко Арсеній Миколайович',
    taxpayer_account_card='1234567890',
    address="м. Чернігів, вул. Доценка, 17, кв. 35",
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
    from_bill=bill_service.read(4),
    from_business=business_service.read(1),
    amount=1000,
    description='Покупка кавоварок',
    kind=RecordKinds.SPENDING,
    sub_kind=RecordSubKinds.REGULAR_SPENDING,
    currency='UAH',
    from_business_category=business_category_service.read(1)
)

business_record_service.create(
    from_bill=bill_service.read(4),
    from_business=business_service.read(1),
    amount=70,
    description='Продаж кави',
    kind=RecordKinds.INCOME,
    sub_kind=RecordSubKinds.CASH,
    currency='UAH',
    from_business_category=business_category_service.read(1)
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
########################################################################################################################
# create group records
group_record_service.create(
    from_bill=bill_service.read(1),
    from_group=group_service.read(1),
    amount=1000,
    description='Пузата хата',
    kind=RecordKinds.SPENDING,
    currency='UAH',
    from_group_category=group_category_service.read(2)
)
########################################################################################################################
# create user budgets by category and by record

user_budget_service.create(
    name='test1',
    limit=100,
    currency='uah',
    kind=BudgetKinds.BY_CATEGORY,
    from_user=user_service.read(1),
    from_category=user_category_service.read(1)
)
user_budget_service.create(
    name='test2',
    limit=1050,
    currency='uah',
    kind=BudgetKinds.BY_RECORD,
    from_user=user_service.read(1)
)
########################################################################################################################
# create group budgets by category and by record
group_budget_service.create(
    name='group test1',
    limit=100,
    currency='uah',
    kind=BudgetKinds.BY_CATEGORY,
    from_group=group_service.read(1),
    from_category=group_category_service.read(1)
)
group_budget_service.create(
    name='group test2',
    limit=1050,
    currency='uah',
    kind=BudgetKinds.BY_RECORD,
    from_group=group_service.read(1)
)
