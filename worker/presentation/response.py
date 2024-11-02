from typing import List

from pydantic import BaseModel

from measurement.domain.model.value_object import SensorType
from shared_kernel.presentation.response import BaseResponse
from worker.domain.model.value_object import PositionType


class StepDefinitionSchema(BaseModel):
    id: int
    position: PositionType
    duration: int
    period: int
    lead: int
    sensor_type: SensorType

    class Config:
        orm_mode = True
        from_attributes=True


class StepDefinitionResponse(BaseResponse):
    result: List[StepDefinitionSchema]