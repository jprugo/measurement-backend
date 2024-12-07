from __future__ import annotations
from shared_kernel.domain.entity import AggregateRoot
from dataclasses import dataclass
from measurement.domain.model.value_object import SensorType
from worker.domain.model.value_object import PositionType


dataclass(eq=False)
class Event():
    title: str
    description: str

    def __init__(self, title: str, description: str):
         self.title = title
         self.description = description

dataclass(eq=False)
class StepDefinition(AggregateRoot):
    id: int
    position: PositionType
    duration: int
    period: int
    lead: int
    sensor_type: SensorType
    
    @classmethod
    def create(
        cls, 
        position: PositionType,
        duration: int,
        period: int,
        lead: int,
        sensor_type: SensorType,
    ) -> StepDefinition:
        # Action
        return cls(
            position=position,
            duration=duration,
            period=period,
            lead=lead,
            sensor_type=sensor_type,
        )

    def update(
            self, 
            position: PositionType,
            duration: int,
            period: int,
            lead: int,
            sensor_type: SensorType
        ):
            self.position=position
            self.duration=duration
            self.period=period
            self.lead=lead
            self.sensor_type=sensor_type