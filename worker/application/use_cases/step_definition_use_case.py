from typing import Callable, ContextManager, List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from worker.domain.model.aggregate import Event, StepDefinition
from worker.domain.model.value_object import PositionType
from worker.domain.model.step_definition_service import (
    StepDefinitionService,
    CreateStepDefinitionRequest, UpdateStepDefinitionRequest, GetStepDefinitionRequest
)
from worker.infra.repository import StepDefinitionRepository, EventRepository


class StepDefinitionQueryUseCase:
    def __init__(self, repo: StepDefinitionRepository, db_session: Callable[[], ContextManager[Session]]):
        self.repo = repo
        self.db_session = db_session

    def get_all_step_definition(self) -> List[StepDefinition]:
        with self.db_session() as session:
            return self.repo.get_all(session=session)

    def find_by_position(self, position: PositionType) -> List[StepDefinition]:
        with self.db_session() as session:
            sds: List[StepDefinition] = list(
                self.repo.find_by_position(session=session, position=position)
            )
            return sds


class CreateStepDefinitionCommand:
    def __init__(self, service: StepDefinitionService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: CreateStepDefinitionRequest) -> StepDefinition:
        with self.db_session() as session:
            step_definition = self.service.create_step_definition(request, session)
            session.commit()
            return step_definition


class UpdateStepDefinitionCommand:
    def __init__(self, service: StepDefinitionService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: UpdateStepDefinitionRequest) -> StepDefinition:
        with self.db_session() as session:
            step_definition = self.service.update_step_definition(request, session)
            session.commit()
            return step_definition


class DeleteStepDefinitionCommand:
    def __init__(self, service: StepDefinitionService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: GetStepDefinitionRequest) -> StepDefinition:
        with self.db_session() as session:
            self.service.delete_step_definition(request, session)
            session.commit()


class EventQueryUseCase:
    def __init__(self, repo: EventRepository):
        self.repo = repo

    def get(self) -> Event:
       return self.repo.get()
    

class CreateEventCommandRequest(BaseModel):
    title: str
    description: str


class CreateEventCommand:
    def __init__(self, repo: EventRepository):
        self.repo = repo

    def execute(self, request: CreateEventCommandRequest) -> Event:
        self.repo.add(
            Event(
                title=request.title,
                description=request.description,
            )
        )