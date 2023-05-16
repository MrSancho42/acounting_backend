from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RecordKinds(Enum):
    INCOME = 'INCOME'
    SPENDING = 'SPENDING'
    TRANSFER = 'TRANSFER'


@dataclass
class User:
    pk_user: int | None

    name: str
    email: str
    password: str

    businesses: list = field(default_factory=list)
    bills: list = field(default_factory=list)
    creates: list = field(default_factory=list)
    user_categories: list = field(default_factory=list)


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

    amount: float
    description: str
    kind: RecordKinds
    creation_time: datetime
    currency: str

    from_bill: Bill


@dataclass
class BusinessRecord(Record):
    fk_business: int | None

    from_business: Business


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

    from_user: User

    sub_categories: list = field(default_factory=list)


@dataclass()
class BusinessCategory(Category):
    pk_business_category: int | None
    fk_business: int | None

    from_business: Business

    sub_categories: list = field(default_factory=list)


@dataclass()
class SubCategory:
    name: str
    ico: str
    colour: str


@dataclass()
class UserSubCategory(SubCategory):
    pk_user_sub_category: int | None
    fk_user_category: int | None

    depends_on_user_category: UserCategory


@dataclass()
class BusinessSubCategory(SubCategory):
    pk_business_sub_category: int | None
    fk_business_category: int | None

    depends_on_business_category: BusinessCategory


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
class GroupRecord:
    pk_group_record: int | None
    fk_group: int | None
    fk_record: int | None

    from_group: Group
    from_record: Record


@dataclass()
class GroupCategory(Category):
    pk_group_category: int | None
    fk_group: int | None

    from_group: Group

    sub_categories: list = field(default_factory=list)


@dataclass()
class GroupSubCategory(Category):
    pk_group_sub_category: int | None
    fk_group_category: int | None

    depends_on_group_category: GroupCategory


@dataclass()
class Budget:
    name: str
    limit: float
    currency: str


@dataclass()
class UserBudgetByCategory(Budget):
    pk_user_budget_by_category: int | None
    fk_user: int | None
    fk_user_category: int | None

    from_user_category: UserCategory
    visibility_to: User


@dataclass()
class UserBudgetBySubCategory(Budget):
    pk_user_budget_by_sub_category: int | None
    fk_user: int | None
    fk_user_sub_category: int | None

    from_user_sub_category: UserSubCategory
    visibility_to: User


@dataclass()
class GroupBudgetByCategory(Budget):
    pk_group_budget_by_category: int | None
    fk_group: int | None
    fk_group_category: int | None

    from_group_category: GroupCategory
    visibility_to: Group


@dataclass()
class GroupBudgetBySubCategory(Budget):
    pk_group_budget_by_sub_category: int | None
    fk_group: int | None
    fk_group_sub_category: int | None

    from_group_sub_category: GroupSubCategory
    visibility_to: Group


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
    fk_user: int | None
    fk_record: int | None

    from_user: User
    from_record: Record


@dataclass()
class GroupRecordBudget:
    pk_group_record_budget: int | None
    fk_group: int | None
    fk_record: int | None

    from_group: Group
    from_record: Record
