from __future__ import annotations

from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass

from measurement.domain.model.value_object import MeasureType, Unit, SensorType
from shared_kernel.domain.entity import AggregateRoot, Aggregate


dataclass(eq=False)
class Measure(AggregateRoot):
    id: int
    value: float
    created_at: datetime
    measure_type: MeasureType
    detail: Optional[str] = None

    @classmethod
    def create(
        cls, value: float, measure_type: MeasureType, detail: Optional[str] = None, created_at=Optional[datetime]
    ) -> Measure:
        return cls(
            value=value,
            created_at= datetime.now() if not created_at else created_at,
            measure_type=measure_type,
            detail=detail,
        )


# Sensor
dataclass(eq=False)
class MeasurementSpec(Aggregate):
    measure_type: MeasureType
    unit: Unit

    @classmethod
    def create(
        cls, measure_type: MeasureType, unit: Unit
    ) -> Measure:
        return cls(
            measure_type=measure_type,
            unit=unit,
        )


dataclass(eq=False)
class Sensor(AggregateRoot):
    id: int
    brand: str
    reference: str
    sensor_type: SensorType
    measurement_specs: List[MeasurementSpec]

    @classmethod
    def create(
        cls, brand: str, reference: str, sensor_type: SensorType, measure_sensor_details: List[MeasurementSpec]
    ) -> Measure:
        return cls(
            brand=brand,
            reference=reference,
            sensor_type=sensor_type,
            measurement_specs=measure_sensor_details,
        )