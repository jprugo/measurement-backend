from datetime import datetime
from typing import Optional
import strawberry

# Type
@strawberry.type
class MeasurementType:
    id: int
    value: float
    sensor_type: str
    created_at: str

# Input
@strawberry.input
class MeasurementInput():
    sensor_type: str
    value: float

# Input filters
@strawberry.input
class DateInputFilter:
    start_date: datetime
    end_date: datetime

@strawberry.input
class FilterInput:
    created_at: DateInputFilter
    type: Optional[str] = None