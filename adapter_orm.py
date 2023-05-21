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
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False),
)


table_user_category = Table(
    'user_category',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('ico', String(255), nullable=False),
    Column('colour', String(6), nullable=False),

    Column('pk_user_category', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False),
    Column('fk_parent_category', Integer, ForeignKey('user_category.pk_user_category'), nullable=True),
)


table_business_category = Table(
    'business_category',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('ico', String(255), nullable=False),
    Column('colour', String(6), nullable=False),

    Column('pk_business_category', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_business', Integer, ForeignKey('business.pk_business'), nullable=False),
    Column('fk_parent_category', Integer, ForeignKey('business_category.pk_business_category'), nullable=True),
)


table_group_permission = Table(
    'group_permission',
    mapper_registry.metadata,

    Column('permission_description', String(255), nullable=False, unique=True),
    Column('pk_group_permission', Integer, primary_key=True, autoincrement=True, nullable=False),
)


table_group = Table(
    'group',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),

    Column('pk_group', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False),
)


table_user_group_permission = Table(
    'user_group_permission',
    mapper_registry.metadata,

    Column('pk_user_group_permission', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False),
    Column('fk_group', Integer, ForeignKey('group.pk_group'), nullable=False),
    Column('fk_group_permission', Integer, ForeignKey('group_permission.pk_group_permission'), nullable=False),
)


table_group_record = Table(
    'group_record',
    mapper_registry.metadata,

    Column('amount', Float, nullable=False),
    Column('description', String(255), nullable=True),
    Column('kind', Enum(domain.RecordKinds), nullable=False),
    Column('creation_time', DateTime, nullable=False),
    Column('currency', String(5), nullable=False),

    Column('pk_record', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_bill', Integer, ForeignKey('bill.pk_bill'), nullable=False),
    Column('fk_group', Integer, ForeignKey('group.pk_group'), nullable=False),
)


table_group_category = Table(
    'group_category',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('ico', String(255), nullable=False),
    Column('colour', String(6), nullable=False),

    Column('pk_group_category', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_group', Integer, ForeignKey('group.pk_group'), nullable=False),
    Column('fk_parent_category', Integer, ForeignKey('group_category.pk_group_category'), nullable=True)
)


table_user_budget_by_category = Table(
    'user_budget_by_category',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('limit', Float, nullable=False),
    Column('currency', String(5), nullable=False),

    Column('pk_user_budget_by_category', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False),
    Column('fk_user_category', Integer, ForeignKey('user_category.pk_user_category'), nullable=False),
)


table_group_budget_by_category = Table(
    'group_budget_by_category',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('limit', Float, nullable=False),
    Column('currency', String(5), nullable=False),

    Column('pk_group_budget_by_category', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_group', Integer, ForeignKey('group.pk_group'), nullable=False),
    Column('fk_group_category', Integer, ForeignKey('group_category.pk_group_category'), nullable=False),
)


table_user_budget = Table(
    'user_budget',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('limit', Float, nullable=False),
    Column('currency', String(5), nullable=False),

    Column('pk_user_budget', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False),
)


table_group_budget = Table(
    'group_budget',
    mapper_registry.metadata,

    Column('name', String(255), nullable=False),
    Column('limit', Float, nullable=False),
    Column('currency', String(5), nullable=False),

    Column('pk_group_budget', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_group', Integer, ForeignKey('group.pk_group'), nullable=False),
)


table_user_record_budget = Table(
    'user_record_budget',
    mapper_registry.metadata,

    Column('pk_user_record_budget', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_user', Integer, ForeignKey('user.pk_user'), nullable=False),
    Column('fk_record', Integer, ForeignKey('record.pk_record'), nullable=False),
)


table_group_record_budget = Table(
    'group_record_budget',
    mapper_registry.metadata,

    Column('pk_group_record_budget', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('fk_group', Integer, ForeignKey('group.pk_group'), nullable=False),
    Column('fk_record', Integer, ForeignKey('record.pk_record'), nullable=False),
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
            'from_user': relationship(domain.User, backref='user_categories'),
            'from_parent': relationship(
                domain.UserCategory,
                backref='child_categories',
                remote_side=table_user_category.c.pk_user_category
            )
        }
    )

    mapper_registry.map_imperatively(
        domain.BusinessCategory,
        table_business_category,
        properties={
            'from_business': relationship(domain.Business, backref='business_categories'),
            'from_parent': relationship(
                domain.BusinessCategory,
                backref='child_categories',
                remote_side=table_business_category.c.pk_business_category
            )
        }
    )

    mapper_registry.map_imperatively(
        domain.GroupPermission,
        table_group_permission
    )

    mapper_registry.map_imperatively(
        domain.Group,
        table_group,
        properties={'owner': relationship(domain.User, backref='groups')}
    )

    mapper_registry.map_imperatively(
        domain.UserGroupPermission,
        table_user_group_permission,
        properties={
            'permission_owner': relationship(domain.User, backref='granted_permissions'),
            'permission_to': relationship(domain.Group, backref='members'),
            'permission_granted': relationship(domain.GroupPermission, backref='granted_to')
        },
    )

    mapper_registry.map_imperatively(
        domain.GroupRecord,
        table_group_record,
        properties={
            'from_bill': relationship(domain.Bill, backref='group_records'),
            'from_group': relationship(domain.Group, backref='records')
        },
    )

    mapper_registry.map_imperatively(
        domain.GroupCategory,
        table_group_category,
        properties={
            'from_group': relationship(domain.Group, backref='groups_categories'),
            'from_parent': relationship(
                domain.GroupCategory,
                backref='child_categories',
                remote_side=table_group_category.c.pk_group_category
            )
        }
    )

    mapper_registry.map_imperatively(
        domain.UserBudgetByCategory,
        table_user_budget_by_category,
        properties={
            'visibility_to': relationship(domain.User, backref='budgets_by_categories'),
            'from_user_category': relationship(domain.UserCategory, backref='related_user_budgets')
        }
    )

    mapper_registry.map_imperatively(
        domain.GroupBudgetByCategory,
        table_group_budget_by_category,
        properties={
            'visibility_to': relationship(domain.Group, backref='budgets_by_categories'),
            'from_group_category': relationship(domain.GroupCategory, backref='related_group_budgets')
        }
    )

    mapper_registry.map_imperatively(
        domain.UserBudget,
        table_user_budget,
        properties={
            'from_user': relationship(domain.User, backref='related_user_budgets')
        }
    )

    mapper_registry.map_imperatively(
        domain.GroupBudget,
        table_group_budget,
        properties={
            'from_group': relationship(domain.Group, backref='related_group_budgets')
        }
    )

    mapper_registry.map_imperatively(
        domain.UserRecordBudget,
        table_user_record_budget,
        properties={
            'from_record': relationship(domain.Record, backref='related_budget_user'),
            'from_user': relationship(domain.User, backref='related_budget_record')
        }
    )

    mapper_registry.map_imperatively(
        domain.GroupRecordBudget,
        table_group_record_budget,
        properties={
            'from_record': relationship(domain.Record, backref='related_budget_group'),
            'from_group': relationship(domain.Group, backref='related_budget_record')
        }
    )
