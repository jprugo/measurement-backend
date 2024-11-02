from __future__ import annotations
from shared_kernel.domain.value_object import ValueObject
import enum
from pydantic import BaseModel
from typing import List


class MeasureType(ValueObject, str, enum.Enum):
    ISOLATION = "ISOLATION"
    RESISTANCE = "RESISTANCE"
    TEMPERATURE = "TEMPERATURE"
    PRESSURE = "PRESSURE"
    VIBRATION = "VIBRATION"
    BATTERY = "BATTERY"


class SensorType(ValueObject, str, enum.Enum):
    ISO = "ISO"
    RES = "RES"
    WELL = "WELL"

    def __init__(self, measure_types: List[MeasureType]):
        self.measure_types = measure_types

    @classmethod
    def get_measure_types(cls, sensor_type):
        if sensor_type == cls.ISO:
            return [MeasureType.ISOLATION]
        elif sensor_type == cls.RES:
            return [MeasureType.RESISTANCE]
        elif sensor_type == cls.WELL:
            return [MeasureType.RESISTANCE, MeasureType.VIBRATION, MeasureType.TEMPERATURE]
        else:
            return []


class MeasureDeviceResponse(ValueObject, BaseModel):
    measures: List[DeviceMeasure]


class DeviceMeasure(ValueObject, BaseModel):
    value: float
    measure_type: MeasureType
    detail: str

    @classmethod
    def create(
        cls, value: float, description: str, measure_type: MeasureType, detail: str
    ) -> DeviceMeasure:
        # Action
        return cls(
            value = value,
            description= description,
            measure_type= measure_type,
            detail= detail
        )
