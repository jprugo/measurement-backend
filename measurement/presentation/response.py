from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from measurement.domain.model.value_object import MeasureType, SensorType, Unit
from shared_kernel.presentation.response import BaseResponse
import enum


class MeasurementSchema(BaseModel):
    id: int
    value: float
    created_at: datetime
    measure_type: MeasureType
    unit: Optional[str] = None
    detail: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes=True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SensorTypeResponse(BaseResponse):
    result:  List[SensorType]


class MeasureTypeResponse(BaseResponse):
    result:  List[MeasureType]


class UnitSchema(BaseModel):
    name: str
    value: str


class UnitResponse(BaseResponse):
    result:  List[UnitSchema]


class MeasurementSpecSchema(BaseModel):
    measure_type: MeasureType
    unit: Unit


class SensorSchema(BaseModel):
    id: int
    brand: str
    reference: str
    sensor_type: SensorType
    measurement_spec: List[MeasurementSpecSchema]


class SensorsResponse(BaseResponse):
    result: List[SensorSchema]


class SensorResponse(BaseResponse):
    result: Optional[SensorSchema]


class MeasurementResponse(BaseResponse):
    result: List[MeasurementSchema] = None

class MeasurementResponse2(BaseResponse):
    result: Optional[MeasurementSchema] = None

class ModBusID(enum.Enum):
    INTAKE_PRESSURE = enum.auto()
    DISCHARGE_PRESSURE = enum.auto()

    INTAKE_TEMPERATURE = enum.auto()
    ENGINE_TEMPERATURE = enum.auto()
    
    X_VIBRATION = enum.auto()
    Z_VIBRATION = enum.auto()

    TOOL_CURRENT = enum.auto()
    TOOL_VOLTAGE = enum.auto()

    RESISTANCE_1 = enum.auto()
    RESISTANCE_2 = enum.auto()
    RESISTANCE_3 = enum.auto()

    BATTERY = enum.auto()
    TENSION_DETECTED = enum.auto()

    ISOLATION = enum.auto()
    ISOLATION_CURRENT = enum.auto()
    ISOLATION_VOLTAGE = enum.auto()

def get_last_measurement_id(
        measure_type: MeasureType,
        detail: Optional[str] = None
    ):
    if measure_type == MeasureType.PRESSURE:
        if detail == "C":
            return ModBusID.INTAKE_PRESSURE
        else:
            return ModBusID.DISCHARGE_PRESSURE
    elif measure_type == MeasureType.TEMPERATURE:
        if detail == "C":
            return ModBusID.INTAKE_TEMPERATURE
        else:
            return ModBusID.ENGINE_TEMPERATURE
    elif measure_type == MeasureType.VIBRATION:
        if detail == "X":
            return ModBusID.X_VIBRATION
        else:
            return ModBusID.Z_VIBRATION
    elif measure_type == MeasureType.ISOLATION:
        return ModBusID.ISOLATION
    elif measure_type == MeasureType.RESISTANCE:
        if detail == "1":
            return ModBusID.RESISTANCE_1
        elif detail == "2":
            return ModBusID.RESISTANCE_2
        else:
            return ModBusID.RESISTANCE_3
    elif measure_type == MeasureType.BATTERY:
        return ModBusID.BATTERY
    elif measure_type == MeasureType.ISOLATION_VOLTAGE:
        return ModBusID.ISOLATION_VOLTAGE
    elif measure_type == MeasureType.LEAKEGE_CURRENT:
        return ModBusID.ISOLATION_CURRENT
    elif measure_type == MeasureType.TOOL_CURRENT:
        return ModBusID.TOOL_CURRENT
    elif measure_type == MeasureType.TOOL_VOLTAGE:
        return ModBusID.TOOL_VOLTAGE
        
def get_last_measurement_detail(
        measure_type: MeasureType,
        detail: Optional[str] = None
):
    if measure_type == MeasureType.RESISTANCE:
        if detail == "1":
            return "A-B"
        elif detail == "2":
            return "B-C"
        else:
            return "C-A"
    elif measure_type == MeasureType.PRESSURE:
        if detail == "C":
            return "I"
        else:
            return detail
    elif measure_type == MeasureType.TEMPERATURE:
        if detail == "C":
            return "I"
        else:
            return detail
    else:
        return detail
    

class LastMeasurementSchema(BaseModel):
    id: ModBusID
    value: float
    created_at: datetime
    measure_type: MeasureType
    unit:  Optional[Unit] =  None
    detail: Optional[str] = None


class LastMeasurementResponse(BaseResponse):
    result: List[LastMeasurementSchema] = None
