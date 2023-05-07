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
