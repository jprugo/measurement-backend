from typing import Callable, ContextManager, List

from sqlalchemy.orm import Session

from alarming.domain.model.aggregate import Alarm, AlarmDefinition
from alarming.domain.model.services import (
    AlarmDefinitionService, AlarmService,
    # Requests
    RegisterAlarmDefinitionRequest, RegisterAlarmRequest,
    UpdateAlarmDefinitionRequest, GetAlarmDefinitionRequest,
)
from alarming.infra.repository import AlarmDefinitionRepository, AlarmRepository
from measurement.domain.model.value_object import MeasureType

class AlarmQueryUseCase:
    def __init__(self, repo: AlarmRepository, db_session: Callable[[], ContextManager[Session]]):
        self.repo = repo
        self.db_session = db_session

    def get_alarms(self) -> List[Alarm]:
        with self.db_session() as session:
            alarms: List[Alarm] = list(
                self.repo.get_all(session=session)
            )
            return alarms


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
    
    def get_alarms_definition_by_measure_type(self, measure_type: MeasureType) -> List[AlarmDefinition]:
        with self.db_session() as session:
            alarms_def: List[AlarmDefinition] = list(
                self.repo.find_by_measure_type(session=session, measure_type= measure_type)
            )
            return alarms_def


class CreateAlarmCommand:
    def __init__(self, service: AlarmService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: RegisterAlarmRequest) -> Alarm:
        with self.db_session() as session:
            alarm = self.service.create_alarm(request, session)
            session.commit()
            return alarm


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
