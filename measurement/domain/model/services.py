from typing import Optional

from sqlalchemy.orm import Session

from measurement.domain.model.aggregate import Measure
from measurement.domain.model.value_object import MeasureType
from measurement.infra.repository import MeasurementRepository
from pydantic import BaseModel
from datetime import datetime


class CreateMeasurementRequest(BaseModel):
    value: float
    measure_type: MeasureType
    detail: Optional[str] = None


class GetMeasurementRequest(BaseModel):
    measure_type: MeasureType
    start_date: datetime
    end_date: datetime
    detail: Optional[str] = None


class MeasurementService:
    def __init__(self, repo: MeasurementRepository):
        self.repo = repo

    def create_measure(self, session: Session, request: CreateMeasurementRequest) -> Measure:
        measure = Measure.create(
            value= request.value,
            measure_type= request.measure_type,
            detail= request.detail
        ) 
        self.repo.add(instance=measure, session=session)
        return measure
