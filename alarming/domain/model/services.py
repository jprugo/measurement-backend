from sqlalchemy.orm import Session

from alarming.domain.model.value_object import AlarmType
from measurement.domain.model.value_object import MeasureType

from alarming.domain.model.aggregate import Alarm, AlarmDefinition
from alarming.infra.repository import AlarmDefinitionRepository, AlarmRepository
from pydantic import BaseModel

class RegisterAlarmRequest(BaseModel):
    value: float
    config_value: float
    alarm_type: AlarmType
    measure_type: MeasureType


class UpdateAlarmDefinitionRequest(BaseModel):
    id: int
    new_value: float
    new_alarm_type: AlarmType
    new_sound_path: str


class GetAlarmDefinitionRequest(BaseModel):
    id: int


class RegisterAlarmDefinitionRequest(BaseModel):
    value: float
    alarm_type: AlarmType
    measure_type: MeasureType
    sound_path: str


class AlarmService:
    
    def __init__(self, repo: AlarmRepository):
        self.repo = repo


    def create_alarm(self, request: RegisterAlarmRequest, session: Session) -> Alarm:
        alarm = Alarm.create(
            measure_value= request.value,
            config_value= request.config_value,
            measure_type= request.measure_type,
            alarm_type= request.alarm_type,
        )
        self.repo.add(instance=alarm, session=session)
        return alarm


class AlarmDefinitionService:

    def __init__(self, repo: AlarmDefinitionRepository):
        self.repo = repo


    def create_alarm_definition(self, request: RegisterAlarmDefinitionRequest, session: Session) -> AlarmDefinition:
        alarm_definition = AlarmDefinition.create(
            config_value= request.value,
            sound_path= request.sound_path,
            measure_type= request.measure_type,
            alarm_type= request.alarm_type
        )
        self.repo.add(instance=alarm_definition, session=session)
        return alarm_definition


    def update_alarm_definition(self, request: UpdateAlarmDefinitionRequest, session: Session) -> AlarmDefinition:
        alarm_definition = self.repo.get_by_id(entity_id=request.id, session=session)
        if not alarm_definition:
            raise ValueError("Alarm definition not found")
        alarm_definition.update(config_value= request.new_value, alarm_type= request.new_alarm_type, sound_path= request.new_sound_path)
        self.repo.add(instance=alarm_definition, session=session)
        return alarm_definition

    def delete_alarm_definition(self, request: GetAlarmDefinitionRequest, session: Session) -> None:
        alarm_definition = self.repo.get_by_id(entity_id=request.id, session=session)
        if not alarm_definition:
            raise ValueError("Alarm definition not found")
        self.repo.delete(session=session, instance=alarm_definition)
