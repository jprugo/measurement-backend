from sqlalchemy.orm import Session

from configuration.infra.repository import ConfigurationRepository
from configuration.domain.model.aggregate import Configuration
from configuration.domain.model.value_object import TreatmentAs

from pydantic import BaseModel


class UpdateConfigurationRequest(BaseModel):
    id: int
    value: str


class CreateConfigurationRequest(BaseModel):
    name: str
    value: str
    treatment_as: TreatmentAs

class GetConfigurationByIdRequest(BaseModel):
    id: int


class ConfigurationService:
    def __init__(self, repo: ConfigurationRepository):
        self.repo = repo

    def create_configuration(self, request: CreateConfigurationRequest, session: Session) -> Configuration:
        configuration = Configuration.create(
            name= request.name,
            value= request.value,
            treatment_as= request.treatment_as
        )
        self.repo.add(instance=configuration, session=session)
        return configuration

    def update_configuration(self, request: UpdateConfigurationRequest, session: Session) -> Configuration:
        configuration = self.repo.get_by_id(entity_id=request.id, session=session)
        if not configuration:
            raise ValueError("Configuration not found")
        configuration.update(value= request.value)
        self.repo.add(instance=configuration, session=session)
        return configuration

    def delete_configuration(self, request: GetConfigurationByIdRequest, session: Session) -> Configuration:
        configuration = self.repo.get_by_id(entity_id=request.id, session=session)
        if not configuration:
            raise ValueError("Configuration not found")
        self.repo.delete(instance=configuration, session=session)
        return configuration
