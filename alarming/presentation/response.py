from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime

from alarming.domain.model.value_object import AlarmType
from measurement.domain.model.value_object import MeasureType
from shared_kernel.presentation.response import BaseResponse


class AlarmSchema(BaseModel):
    id: int
    measure_value: float
    measure_type: MeasureType
    alarm_type: AlarmType
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes=True


class AlarmResponse(BaseResponse):
    result: List[AlarmSchema]


class AlarmDefinitionSchema(BaseModel):
    id: int
    config_value: float
    sound_path: str
    measure_type: MeasureType
    alarm_type: AlarmType
    created_at: datetime
    updated_at: Optional[datetime]
    enabled: bool

    class Config:
        orm_mode = True
        from_attributes=True


class AlarmDefinitionResponse(BaseResponse):
    result: List[AlarmDefinitionSchema]