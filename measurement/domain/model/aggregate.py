from __future__ import annotations

from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from measurement.domain.model.value_object import MeasureType
from shared_kernel.domain.entity import AggregateRoot

dataclass(eq=False)
class Measure(AggregateRoot):
    id: int
    value: float
    created_at: datetime
    measure_type: MeasureType
    detail: Optional[str] = None

    @classmethod
    def create(
        cls, value: float, measure_type: MeasureType, detail: Optional[str] = None
    ) -> Measure:
        # Action
        return cls(
            value = value,
            created_at= datetime.now(),
            measure_type=measure_type,
            detail=detail,
        )