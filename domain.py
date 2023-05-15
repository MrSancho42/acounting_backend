from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RecordKinds(Enum):
    INCOME = 'INCOME'
    SPENDING = 'SPENDING'
    TRANSFER = 'TRANSFER'


@dataclass
class User:
    pk_user: int

    name: str
    email: str
    password: str

    businesses: list = field(default_factory=list)


class UserException:

    class MailAlreadyInUse(Exception):
        ...

    class UserNotFound(Exception):
        ...


@dataclass
class Business:
    pk_business: int
    fk_user: int

    name: str

    owner: User


@dataclass
class Bill:
    pk_bill: int
    fk_user: int

    name: str
    amount: float
    currency: str
    is_for_business: bool

    owner: User


@dataclass
class Record:
    pk_record: int
    fk_bill: int

    amount: float
    description: str
    kind: RecordKinds
    creation_time: datetime
    currency: str

    from_bill: Bill


@dataclass
class BusinessRecord(Record):
    fk_business: int

    from_business: Business


@dataclass()
class Employee:
    pk_employee: int

    name: str


@dataclass()
class BusinessEmployee:
    pk_id: int
    fk_business: int
    fk_employee: int


@dataclass()
class Credit:
    pk_credit: int
    fk_user: int

    name: str
    total_cost: float
    total_size: float
    due_date: datetime

    credit_owner: User


@dataclass()
class Category:
    pk_category: int

    name: str
    ico: str
    colour: str


@dataclass()
class UserCategory:
    pk_user_category: int
    fk_user: int
    fk_category: int

    from_user: User
    from_category: Category


@dataclass()
class BusinessCategory:
    pk_business_category: int
    fk_business: int
    fk_category: int

    from_business: Business
    from_category: Category


@dataclass()
class SubCategory:
    pk_sub_category: int
    fk_category: int

    name: str
    ico: str
    colour: str

    depends_on_category: Category


@dataclass()
class UserSubCategory:
    pk_user_sub_category: int
    fk_user: int
    fk_sub_category: int

    from_user: User
    from_sub_category: SubCategory


@dataclass()
class BusinessSubCategory:
    pk_business_sub_category: int
    fk_business: int
    fk_sub_category: int

    from_business: Business
    from_sub_category: SubCategory
