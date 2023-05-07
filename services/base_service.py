from abc import abstractmethod

from pydantic import BaseModel

from repository import SqlAlchemyRepository


class BaseService:
    repository: SqlAlchemyRepository = None

    def __init__(self, repository):
        self.repository = repository

    @abstractmethod
    def create(self, *args, **kwargs): ...

    @abstractmethod
    def read(self, *args, **kwargs): ...

    def update(self, entity, new_data: BaseModel | dict):
        if isinstance(new_data, BaseModel):
            new_data = new_data.dict()

        for key, value in new_data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        self.repository.apply_changes()

    @abstractmethod
    def delete(self, *args, **kwargs): ...
