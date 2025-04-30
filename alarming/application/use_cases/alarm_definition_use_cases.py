from typing import Callable, ContextManager, List

from sqlalchemy.orm import Session

from alarming.domain.model.aggregate import  AlarmDefinition
from alarming.domain.model.services import (
    AlarmDefinitionService,
    # Requests
    RegisterAlarmDefinitionRequest,
    UpdateAlarmDefinitionRequest, GetAlarmDefinitionRequest,
)
from alarming.infra.repository import AlarmDefinitionRepository
from measurement.domain.model.value_object import MeasureType


class AlarmDefinitionQueryUseCase:
    def __init__(self, repo: AlarmDefinitionRepository, db_session: Callable[[], ContextManager[Session]]):
        self.repo = repo
        self.db_session = db_session

    def get_alarms_definition(self) -> List[AlarmDefinition]:
        with self.db_session() as session:
            alarms_def: List[AlarmDefinition] = list(
                self.repo.get_all(session=session)
            )
            return alarms_def
    
    def get_alarms_definition_by_measure_type(
            self,
            measure_type: MeasureType,
            measure_detail: str
        ) -> List[AlarmDefinition]:
        with self.db_session() as session:
            alarms_def: List[AlarmDefinition] = list(
                self.repo.find_by_measure_type_and_detail(
                    session=session,
                    measure_type=measure_type,
                    measure_detail=measure_detail
                )
            )
            return alarms_def


class CreateAlarmDefinitionCommand:
    def __init__(self, service: AlarmDefinitionService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: RegisterAlarmDefinitionRequest) -> AlarmDefinition:
        with self.db_session() as session:
            alarm_definition = self.service.create_alarm_definition(request, session)
            session.commit()
            return alarm_definition


class UpdateAlarmDefinitionCommand:
    def __init__(self, service: AlarmDefinitionService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: UpdateAlarmDefinitionRequest) -> AlarmDefinition:
        with self.db_session() as session:
            alarm_definition = self.service.update_alarm_definition(request, session)
            session.commit()
            return alarm_definition


class DeleteAlarmDefinitionCommand:
    def __init__(self, service: AlarmDefinitionService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: GetAlarmDefinitionRequest) -> None:
        with self.db_session() as session:
            self.service.delete_alarm_definition(request, session)
            session.commit()
