from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, Float, Boolean, Enum, DateTime
from sqlalchemy.orm import registry, relationship

import domain

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


table_user = Table(
    'user',
    mapper_registry.metadata,

    Column('name', String(255)),
    Column('email', String(255), unique=True),
    Column('password', String(255)),

    Column('pk_user', Integer, primary_key=True, autoincrement=True),
)


table_business = Table(
    'business',
    mapper_registry.metadata,

    Column('name', String(255)),

    Column('pk_business', Integer, primary_key=True, autoincrement=True),
    Column('fk_user', Integer, ForeignKey('user.pk_user')),
)


table_bill = Table(
    'bill',
    mapper_registry.metadata,

    Column('name', String(255)),
    Column('amount', Float),
    Column('currency', String(5)),
    Column('is_for_business', Boolean),

    Column('pk_bill', Integer, primary_key=True, autoincrement=True),
    Column('fk_user', Integer, ForeignKey('user.pk_user')),
)


table_record = Table(
    'record',
    mapper_registry.metadata,

    Column('amount', Float),
    Column('description', String(255)),
    Column('kind', Enum(domain.RecordKinds)),
    Column('creation_time', DateTime),
    Column('currency', String(5)),

    Column('pk_record', Integer, primary_key=True, autoincrement=True),
    Column('fk_bill', Integer, ForeignKey('bill.pk_bill')),
)


table_business_record = Table(
    'business_record',
    mapper_registry.metadata,

    Column('amount', Float),
    Column('description', String(255)),
    Column('kind', Enum(domain.RecordKinds)),
    Column('creation_time', DateTime),
    Column('currency', String(5)),

    Column('pk_record', Integer, primary_key=True, autoincrement=True),
    Column('fk_bill', Integer, ForeignKey('bill.pk_bill')),
    Column('fk_business', Integer, ForeignKey('business.pk_business')),
)


table_employee = Table(
    'employee',
    mapper_registry.metadata,

    Column('name', String(255)),

    Column('pk_employee', Integer, primary_key=True, autoincrement=True)
)


table_business_employee = Table(
    'business_employee',
    mapper_registry.metadata,

    Column('pk_id', Integer, primary_key=True, autoincrement=True),
    Column('fk_business', Integer, ForeignKey('business.pk_business')),
    Column('fk_employee', Integer, ForeignKey('employee.pk_employee'))
)


table_credit = Table(
    'credit',
    mapper_registry.metadata,

    Column('name', String(255)),
    Column('total_cost', Float),
    Column('total_size', Float),
    Column('due_date', DateTime),

    Column('pk_credit', Integer, primary_key=True, autoincrement=True),
    Column('fk_user', Integer, ForeignKey('user.pk_user'))
)


table_category = Table(
    'category',
    mapper_registry.metadata,

    Column('name', String(255)),
    Column('ico', String(255)),
    Column('colour', String(6)),

    Column('pk_category', Integer, primary_key=True, autoincrement=True)
)


table_user_category = Table(
    'user_category',
    mapper_registry.metadata,

    Column('pk_user_category', Integer, primary_key=True, autoincrement=True),
    Column('fk_user', Integer, ForeignKey('user.pk_user')),
    Column('fk_category', Integer, ForeignKey('category.pk_category'))
)


table_business_category = Table(
    'business_category',
    mapper_registry.metadata,

    Column('pk_business_category', Integer, primary_key=True, autoincrement=True),
    Column('fk_business', Integer, ForeignKey('business.pk_business')),
    Column('fk_category', Integer, ForeignKey('category.pk_category'))
)


table_sub_category = Table(
    'sub_category',
    mapper_registry.metadata,

    Column('name', String(255)),
    Column('ico', String(255)),
    Column('colour', String(6)),

    Column('pk_sub_category', Integer, primary_key=True, autoincrement=True),
    Column('fk_category', Integer, ForeignKey('category.pk_category'))
)


table_user_sub_category = Table(
    'user_sub_category',
    mapper_registry.metadata,

    Column('pk_user_sub_category', Integer, primary_key=True, autoincrement=True),
    Column('fk_user', Integer, ForeignKey('user.pk_user')),
    Column('fk_sub_category', Integer, ForeignKey('sub_category.pk_sub_category'))
)


table_business_sub_category = Table(
    'business_sub_category',
    mapper_registry.metadata,

    Column('pk_business_sub_category', Integer, primary_key=True, autoincrement=True),
    Column('fk_business', Integer, ForeignKey('business.pk_business')),
    Column('fk_sub_category', Integer, ForeignKey('sub_category.pk_sub_category'))
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
    )

    mapper_registry.map_imperatively(
        domain.BusinessEmployee,
        table_business_employee,
    )

    mapper_registry.map_imperatively(
        domain.Credit,
        table_credit,
        properties={'credit_owner': relationship(domain.User, backref='credits')}
    )

    mapper_registry.map_imperatively(
        domain.Category,
        table_category,
    )

    mapper_registry.map_imperatively(
        domain.UserCategory,
        table_user_category,
        properties={
            'from_user': relationship(domain.User, backref='user_categories'),
            'from_category': relationship(domain.Category, backref='user_categories')
        }
    )

    mapper_registry.map_imperatively(
        domain.BusinessCategory,
        table_business_category,
        properties={
            'from_business': relationship(domain.Business, backref='business_categories'),
            'from_category': relationship(domain.Category, backref='business_categories')
        }
    )

    mapper_registry.map_imperatively(
        domain.SubCategory,
        table_sub_category,
        properties={
            'depends_on_category': relationship(domain.Category, backref='category_sub_categories')
        }
    )

    mapper_registry.map_imperatively(
        domain.UserSubCategory,
        table_user_sub_category,
        properties={
            'from_user': relationship(domain.User, backref='user_sub_categories'),
            'from_sub_category': relationship(domain.SubCategory, backref='user_sub_categories')
        }
    )

    mapper_registry.map_imperatively(
        domain.BusinessSubCategory,
        table_business_sub_category,
        properties={
            'from_business': relationship(domain.Business, backref='business_sub_categories'),
            'from_sub_category': relationship(domain.SubCategory, backref='business_sub_categories')
        }
    )
