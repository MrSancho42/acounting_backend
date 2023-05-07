from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RecordKinds(Enum):
    INCOME = 'INCOME'
    SPENDING = 'SPENDING'
    TRANSFER = 'TRANSFER'


@dataclass
class User:
    name: str
    email: str
    password: str

    businesses: list = field(default_factory=list)
    bills: list = field(default_factory=list)

    pk_user: int = None


class UserException:

    class MailAlreadyInUse(Exception):
        ...

    class UserNotFound(Exception):
        ...


@dataclass
class Business:
    owner: User

    name: str

    pk_business: int = None
    fk_user: int = None


@dataclass
class Bill:
    owner: User

    name: str
    amount: float
    currency: str = 'UAH'
    is_for_business: bool = False

    pk_bill: int = None
    fk_user: int = None


@dataclass
class Record:
    from_bill: Bill

    amount: float
    description: str
    kind: RecordKinds
    creation_time: datetime = datetime.now()
    currency: str = 'UAH'

    pk_record: int = None
    fk_bill: int = None


@dataclass
class BusinessRecord(Record):
    from_business: Business = None

    fk_business: int = None

