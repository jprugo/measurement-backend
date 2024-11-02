from typing import Callable, ContextManager, List

from sqlalchemy.orm import Session

from configuration.domain.model.aggregate import Configuration
from configuration.infra.repository import ConfigurationRepository
from configuration.domain.model.services import (
    ConfigurationService, 
    CreateConfigurationRequest, UpdateConfigurationRequest, GetConfigurationByIdRequest
)
from pydantic import BaseModel

class GetConfigurationRequest(BaseModel):
    name: str


class ConfigurationQueryUseCase:
    def __init__(self, repo: ConfigurationRepository, db_session: Callable[[], ContextManager[Session]]):
        self.repo = repo
        self.db_session = db_session

    def get_configurations(self) -> List[Configuration]:
        with self.db_session() as session:
            configs: List[Configuration] = list(
                self.repo.get_all(session=session)
            )
            return configs

    def get_configuration(self, request: GetConfigurationRequest) -> List[Configuration]:
        with self.db_session() as session:
            configs: List[Configuration] = list(
                self.repo.find_by_name(session=session, name= request.name)
            )
            return configs


class CreateConfigurationCommand:
    def __init__(self, service: ConfigurationService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: CreateConfigurationRequest) -> Configuration:
        with self.db_session() as session:
            configuration = self.service.create_configuration(request, session)
            session.commit()
            return configuration


class UpdateConfigurationCommand:
    def __init__(self, service: ConfigurationService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: UpdateConfigurationRequest) -> Configuration:
        with self.db_session() as session:
            configuration = self.service.update_configuration(request, session)
            session.commit()
            return configuration


class DeleteConfigurationCommand:
    def __init__(self, service: ConfigurationService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: GetConfigurationByIdRequest) -> None:
        with self.db_session() as session:
            self.service.delete_configuration(request, session)
            session.commit()
