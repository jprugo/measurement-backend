from __future__ import annotations
from shared_kernel.domain.entity import AggregateRoot
from alarming.domain.model.value_object import AlarmType
from measurement.domain.model.value_object import MeasureType
from dataclasses import dataclass
from datetime import datetime

dataclass(eq=False)
class AlarmDefinition(AggregateRoot):
    id: int
    config_value: float
    sound_path: str
    created_at: datetime
    updated_at: datetime
    enabled: bool
    # TODO: We are referencing value objects from another context (Measurement)
    measure_type: MeasureType
    measure_detail: str
    # TODO: We are referencing value objects from another context (Alarming)
    alarm_type: AlarmType

    @classmethod
    def create(
        cls,
        config_value: float,
        sound_path: str,
        measure_type: str,
        measure_detail: str,
        alarm_type: str,
    ) -> AlarmDefinition:
        # Action
        return cls(
            config_value = config_value,
            sound_path = sound_path,
            measure_type = MeasureType(measure_type),
            measure_detail=measure_detail,
            alarm_type= AlarmType(alarm_type),
            created_at= datetime.now(),
            enabled = True
        )

    def update(
            self, 
            config_value: float,
            alarm_type: str,
            sound_path: str,
            enabled: bool
        ) -> None:
        self.config_value = config_value
        self.alarm_type = alarm_type
        self.sound_path = sound_path
        self.updated_at = datetime.now()
        self.enabled = enabled


dataclass(eq=False)
class Alarm(AggregateRoot):
    id: int
    measure_value: float
    config_value: float
    created_at: datetime
    # TODO: We are referencing value objects from another context (Measurement)
    measure_type: MeasureType
    # TODO: We are referencing value objects from another context (Alarming)
    alarm_type: AlarmType

    @classmethod
    def create(
        cls,
        measure_value: float,
        config_value: float,
        measure_type: str,
        alarm_type: str
    ) -> Alarm:
        # Action
        return cls(
            measure_value = measure_value,
            config_value= config_value,
            measure_type = MeasureType(measure_type),
            alarm_type= AlarmType(alarm_type),
            created_at= datetime.now()
        )