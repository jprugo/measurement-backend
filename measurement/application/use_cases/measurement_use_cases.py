from typing import Callable, ContextManager, List, Optional

from sqlalchemy.orm import Session

from measurement.domain.model.aggregate import Measure
from measurement.domain.model.value_object import MeasureType
from measurement.infra.api.device_api_service import MeasurementDeviceApiService
from measurement.infra.repository import MeasurementRepository
from measurement.infra.api.device_repository import DeviceMeasureRepository, DeviceMeasure
from measurement.domain.model.services.measurement_service import (
    CreateMeasurementRequest, MeasurementService
)
from datetime import datetime
from pydantic import BaseModel


class GetMeasurementRequest(BaseModel):
    measure_type: MeasureType
    start_date: datetime
    end_date: datetime
    detail: Optional[str] = None

class GetMeasurementByTimeDeltaRequest(BaseModel):
    measure_type: MeasureType
    minutes_ago: int
    detail: Optional[str] = None

class MeasurementQueryUseCase:
    def __init__(self, repo: MeasurementRepository, db_session: Callable[[], ContextManager[Session]]):
        self.repo = repo
        self.db_session = db_session

    def get_measures(self, request: GetMeasurementRequest) -> List[Measure]:
        with self.db_session() as session:
            measures: List[Measure] = self.repo.find_by_sensor_type_detail_and_date_range(
                session=session,
                start_date=request.start_date,
                end_date=request.end_date,
                measure_type=request.measure_type,
                detail= request.detail
            )
            return measures
        
    def get_last_measures(self) -> List[Measure]:
        with self.db_session() as session:
            measures: List[Measure] = self.repo.find_latest_records_for_all_measure_types(session=session)
            return measures
        
    def get_measure_by_time_delta(self, request: GetMeasurementByTimeDeltaRequest) -> Measure:
        with self.db_session() as session:
            measures: List[Measure] = self.repo.find_by_time_delta(
                session=session,
                minutes_ago=request.minutes_ago,
                measure_type=request.measure_type,
                detail= request.detail
            )
            return measures


class CreateMeasurementCommand:
    def __init__(self, service: MeasurementService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: CreateMeasurementRequest) -> Measure:
        with self.db_session() as session:
            measure = self.service.create_measure(session=session, request=request)
            session.commit()
            return measure


class DeviceMeasurementQueryUseCase:
    def __init__(self, repo: DeviceMeasureRepository, api_service: MeasurementDeviceApiService):
        self.repo = repo
        self.api_service = api_service

    def get_measures(self, measure_type: MeasureType) -> List[DeviceMeasure]:
        measures: List[DeviceMeasure] = self.repo.get(self.api_service, sensor_type= measure_type)
        return measures
