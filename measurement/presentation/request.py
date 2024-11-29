from pydantic import BaseModel
from typing import List

from measurement.domain.model.value_object import MeasureType, Unit

class UpdateMeasurementSpecDTO(BaseModel):
    measure_type: MeasureType
    unit: Unit

class UpdateSensorDTO(BaseModel):
    sensor_id: int
    measurement_specs: List[UpdateMeasurementSpecDTO]