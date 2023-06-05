from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RecordKinds(Enum):
    INCOME = 'INCOME'
    SPENDING = 'SPENDING'
    TRANSFER = 'TRANSFER'


class BudgetKinds(Enum):
    BY_CATEGORY = 'BY_CATEGORY'
    BY_RECORD = 'BY_RECORD'


class RecordSubKinds(Enum):
    CASH = 'CASH'
    NON_CASH = 'NON_CASH'
    FREE_RECEIVED = 'FREE_RECEIVED'
    GRANTS = 'GRANTS'

    REGULAR_SPENDING = 'REGULAR_SPENDING'
    REFUND = 'REFUND'


@dataclass
class User:
    pk_user: int | None

    name: str
    email: str
    password: str

    businesses: list = field(default_factory=list)
    bills: list = field(default_factory=list)
    user_categories: list = field(default_factory=list)
    user_budgets: list = field(default_factory=list)
    groups: list = field(default_factory=list)


class UserException:

    class MailAlreadyInUse(Exception):
        ...

    class UserNotFound(Exception):
        ...


@dataclass
class Business:
    pk_business: int | None
    fk_user: int | None

    name: str
    owner_name: str
    taxpayer_account_card: str
    address: str

    owner: User

    records: list = field(default_factory=list)
    employees: list = field(default_factory=list)
    business_categories: list = field(default_factory=list)


@dataclass
class Bill:
    pk_bill: int | None
    fk_user: int | None

    name: str
    amount: float
    currency: str
    is_for_business: bool

    owner: User

    records: list = field(default_factory=list)
    business_records: list = field(default_factory=list)


@dataclass
class Record:
    pk_record: int | None
    fk_bill: int | None
    fk_category: int | None

    amount: float
    description: str
    kind: RecordKinds
    creation_time: datetime
    currency: str

    from_bill: Bill


@dataclass()
class Employee:
    pk_employee: int | None
    fk_business: int | None

    name: str

    from_business: Business


@dataclass()
class Credit:
    pk_credit: int | None
    fk_user: int | None

    name: str
    total_cost: float
    total_size: float
    due_date: datetime

    owner: User


@dataclass()
class Category:
    name: str
    ico: str
    colour: str


@dataclass()
class UserCategory(Category):
    pk_user_category: int | None
    fk_user: int | None
    fk_parent_category: int | None

    from_user: User
    from_parent: Category

    child_categories: list = field(default_factory=list)


@dataclass()
class UserRecord(Record):
    from_user_category: UserCategory


@dataclass()
class BusinessCategory(Category):
    pk_business_category: int | None
    fk_business: int | None
    fk_parent_category: int | None

    from_business: Business
    from_parent: Category

    child_categories: list = field(default_factory=list)


@dataclass()
class BusinessRecord(Record):
    fk_business: int | None

    sub_kind: RecordSubKinds
    from_business: Business
    from_business_category: BusinessCategory


@dataclass()
class GroupPermission:
    pk_group_permission: int | None

    permission_description: str


@dataclass()
class Group:
    pk_group: int | None
    fk_user: int | None

    name: str

    owner: User

    records: list = field(default_factory=list)
    group_categories: list = field(default_factory=list)
    group_budgets: list = field(default_factory=list)


@dataclass()
class UserGroupPermission:
    pk_user_group_permission: int | None
    fk_user:  int | None
    fk_group: int | None
    fk_group_permission: int | None

    permission_owner: User
    permission_to: Group
    permission_granted: GroupPermission


@dataclass()
class GroupCategory(Category):
    pk_group_category: int | None
    fk_group: int | None
    fk_parent_category: int | None

    from_group: Group
    from_parent: Category

    child_categories: list = field(default_factory=list)


@dataclass
class GroupRecord(Record):
    fk_group: int | None

    from_group: Group
    from_group_category: GroupCategory


@dataclass()
class Budget:
    name: str
    limit: float
    currency: str
    kind: BudgetKinds


@dataclass()
class UserBudget(Budget):
    pk_user_budget: int | None
    fk_user: int | None

    from_user: User


@dataclass()
class GroupBudget(Budget):
    pk_group_budget: int | None
    fk_group: int | None

    from_group: Group


@dataclass()
class UserRecordBudget:
    pk_user_record_budget: int | None
    fk_user_budget: int | None
    fk_record: int | None

    from_user_budget: UserBudget
    from_record: UserRecord


@dataclass()
class GroupRecordBudget:
    pk_group_record_budget: int | None
    fk_group_budget: int | None
    fk_record: int | None

    from_group_budget: GroupBudget
    from_record: GroupRecord


@dataclass()
class UserCategoryBudget:
    pk_user_category_budget: int | None
    fk_user_budget: int | None
    fk_user_category: int | None

    from_user_budget: UserBudget
    from_user_category: UserCategory


@dataclass()
class GroupCategoryBudget:
    pk_group_category_budget: int | None
    fk_group_budget: int | None
    fk_group_category: int | None

    from_group_budget: GroupBudget
    from_group_category: GroupCategory
