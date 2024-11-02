from pydantic import BaseModel
from sqlalchemy.orm import Session

from measurement.domain.model.value_object import SensorType

from worker.domain.model.value_object import PositionType
from worker.infra.repository import StepDefinitionRepository
from worker.domain.model.aggregate import StepDefinition


class CreateStepDefinitionRequest(BaseModel):
    position: PositionType
    duration: int
    period: int
    lead: int
    sensor_type: SensorType


class UpdateStepDefinitionRequest(BaseModel):
    id: int
    position: PositionType
    duration: int
    period: int
    lead: int
    sensor_type: SensorType


class GetStepDefinitionRequest(BaseModel):
    id: int


class StepDefinitionService:

    def __init__(self, repo: StepDefinitionRepository):
        self.repo = repo

    def create_step_definition(self, request: CreateStepDefinitionRequest, session: Session) -> StepDefinition:
        step_definition = StepDefinition.create(
            position= request.position,
            duration= request.duration,
            period= request.period,
            lead= request.lead,
            sensor_type= request.sensor_type
        )
        self.repo.add(instance=step_definition, session=session)
        return step_definition

    def update_step_definition(self, request: UpdateStepDefinitionRequest, session: Session) -> StepDefinition:
        step_definition = self.repo.get_by_id(session=session, entity_id=request.id)
        if not step_definition:
            raise ValueError("Step definition not found")
        step_definition.update(
            position= request.position,
            duration= request.duration,
            period= request.period,
            lead= request.lead,
            sensor_type= request.sensor_type
        )
        self.repo.add(instance=step_definition, session=session)
        return step_definition
    

    def delete_step_definition(self, request: GetStepDefinitionRequest, session: Session) -> StepDefinition:
        step_definition = self.repo.get_by_id(session=session, entity_id=request.id)
        if not step_definition:
            raise ValueError("Step definition not found")
        self.repo.delete(instance=step_definition, session=session)
        return step_definition 
