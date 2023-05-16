from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, Float, Boolean, Enum, DateTime
from sqlalchemy.orm import registry, relationship

import domain

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


table_user = Table(
    'user',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('email', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),

    Column('pk_user', Integer, primary_key=True, autoincrement=True, nullable=False),
)


table_business = Table(
    'business',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),

    Column('pk_business', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False),
)


table_bill = Table(
    'bill',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('amount', Float, nullable=False),
    Column('currency', String(5), nullable=False),
    Column('is_for_business', Boolean, nullable=False),

    Column('pk_bill', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False),
)


table_record = Table(
    'record',
    mapper_registry.metadata,

    Column('amount', Float, nullable=False),
    Column('description', String(255), nullable=True),
    Column('kind', Enum(domain.RecordKinds), nullable=False),
    Column('creation_time', DateTime, nullable=False),
    Column('currency', String(5), nullable=False),

    Column('pk_record', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_bill', Integer, ForeignKey('bill.pk_bill'), nullable=False),
)


table_business_record = Table(
    'business_record',
    mapper_registry.metadata,

    Column('amount', Float, nullable=False),
    Column('description', String(255), nullable=True),
    Column('kind', Enum(domain.RecordKinds), nullable=False),
    Column('creation_time', DateTime, nullable=False),
    Column('currency', String(5), nullable=False),

    Column('pk_record', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_bill', Integer, ForeignKey('bill.pk_bill'), nullable=False),
    Column('fk_business', Integer, ForeignKey('business.pk_business'), nullable=False),
)


table_employee = Table(
    'employee',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),

    Column('pk_employee', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_business', Integer, ForeignKey('business.pk_business'), nullable=False),
)


table_credit = Table(
    'credit',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('total_cost', Float, nullable=False),
    Column('total_size', Float, nullable=False),
    Column('due_date', DateTime, nullable=False),

    Column('pk_credit', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False)
)


table_user_category = Table(
    'user_category',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('ico', String(255), nullable=False),
    Column('colour', String(6), nullable=False),

    Column('pk_user_category', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False),
)


table_business_category = Table(
    'business_category',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('ico', String(255), nullable=False),
    Column('colour', String(6), nullable=False),

    Column('pk_business_category', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_business', Integer, ForeignKey('business.pk_business'), nullable=False)
)


table_user_sub_category = Table(
    'user_sub_category',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('ico', String(255), nullable=False),
    Column('colour', String(6), nullable=False),

    Column('pk_user_sub_category', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user_category', Integer, ForeignKey('user_category.pk_user_category'), nullable=False)
)


table_business_sub_category = Table(
    'business_sub_category',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('ico', String(255), nullable=False),
    Column('colour', String(6), nullable=False),

    Column('pk_business_sub_category', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_business_category', Integer, ForeignKey('business_category.pk_business_category'), nullable=False)
)

table_group_permissions = Table(
    'group_permissions',
    mapper_registry.metadata,

    Column('description', String(255), nullable=False, unique=True),
    Column('pk_group_permission', Integer, primary_key=True, autoincrement=True, nullable=False)
)


def mappers():
    mapper_registry.map_imperatively(
        domain.User,
        table_user
    )

    mapper_registry.map_imperatively(
        domain.Business,
        table_business,
        properties={'owner': relationship(domain.User, backref='businesses')}
    )

    mapper_registry.map_imperatively(
        domain.Bill,
        table_bill,
        properties={'owner': relationship(domain.User, backref='bills')}
    )

    mapper_registry.map_imperatively(
        domain.Record,
        table_record,
        properties={'from_bill': relationship(domain.Bill, backref='records')}
    )

    mapper_registry.map_imperatively(
        domain.BusinessRecord,
        table_business_record,
        properties={
            'from_bill': relationship(domain.Bill, backref='business_records'),
            'from_business': relationship(domain.Business, backref='records')
        },
    )

    mapper_registry.map_imperatively(
        domain.Employee,
        table_employee,
        properties={
            'from_business': relationship(domain.Business, backref='employees')
        },
    )

    mapper_registry.map_imperatively(
        domain.Credit,
        table_credit,
        properties={'owner': relationship(domain.User, backref='credits')}
    )

    mapper_registry.map_imperatively(
        domain.UserCategory,
        table_user_category,
        properties={
            'from_user': relationship(domain.User, backref='user_categories')
        }
    )

    mapper_registry.map_imperatively(
        domain.BusinessCategory,
        table_business_category,
        properties={
            'from_business': relationship(domain.Business, backref='business_categories')
        }
    )

    mapper_registry.map_imperatively(
        domain.UserSubCategory,
        table_user_sub_category,
        properties={
            'depends_on_user_category': relationship(domain.UserCategory, backref='sub_categories')
        }
    )

    mapper_registry.map_imperatively(
        domain.BusinessSubCategory,
        table_business_sub_category,
        properties={
            'depends_on_business_category': relationship(domain.BusinessCategory, backref='sub_categories')
        }
    )

    mapper_registry.map_imperatively(
        domain.GroupPermissions,
        table_group_permissions
    )
