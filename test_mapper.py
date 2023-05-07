import adapter_orm
import sqlalchemy
from repository import SqlAlchemyRepository
from services import UserService, BusinessService, BillService

engine = sqlalchemy.create_engine('sqlite:///./db.db')


adapter_orm.metadata.create_all(engine)
adapter_orm.mappers()
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

repository = SqlAlchemyRepository(session)
user_service = UserService(repository)
business_service = BusinessService(repository)
bill_service = BillService(repository)


bill_service.create(owner=user_service.read(12), name='Кредитні кошти', amount=2045.57, is_for_business=False)

print(bill_service.read(2))


# user = user_service.read(1)
#
# user_service.update(1, {'pk_user': 1, 'name': 'string', 'email': 'xxx', 'password': 'string'})
