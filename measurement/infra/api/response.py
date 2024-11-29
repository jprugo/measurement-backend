from __future__ import annotations
from pydantic import BaseModel
from typing import List
from measurement.domain.model.value_object import MeasureType


class MeasureDeviceResponse(BaseModel):
    measures: List[DeviceMeasure]


class DeviceMeasure(BaseModel):
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