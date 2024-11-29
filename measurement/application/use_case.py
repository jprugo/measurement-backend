from typing import Callable, ContextManager, List, Optional

from sqlalchemy.orm import Session

from measurement.domain.model.aggregate import Measure, Sensor
from measurement.domain.model.value_object import MeasureType
from measurement.infra.api.device_api_service import DeviceApiService
from measurement.infra.repository import MeasurementRepository, SensorRepository
from measurement.infra.api.device_repository import DeviceMeasureRepository, DeviceMeasure
from measurement.domain.model.services import (
    CreateMeasurementRequest, CreateSensorRequest, MeasurementService, 
    SensorService
)
from datetime import datetime
from pydantic import BaseModel


class GetMeasurementRequest(BaseModel):
    measure_type: MeasureType
    start_date: datetime
    end_date: datetime
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
    def __init__(self, repo: DeviceMeasureRepository, api_service: DeviceApiService):
        self.repo = repo
        self.api_service = api_service

    def get_measures(self, measure_type: MeasureType) -> List[DeviceMeasure]:
        measures: List[DeviceMeasure] = self.repo.get(self.api_service, sensor_type= measure_type)
        return measures


# Sensor
class GetSensorByIdRequest(BaseModel):
    id: int


class DeleteSensorCommand:
    def __init__(self, service: SensorService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: GetSensorByIdRequest) -> Measure:
        with self.db_session() as session:
            measure = self.service.delete_sensor(session=session, request=request)
            session.commit()
            return measure


class CreateSensorCommand:
    def __init__(self, service: SensorService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: CreateSensorRequest) -> Measure:
        with self.db_session() as session:
            measure = self.service.create_sensor(session=session, request=request)
            session.commit()
            return measure


class GetSensorRequest(BaseModel):
    measure_type: MeasureType


class SensorQueryUseCase:
    def __init__(self, repo: SensorRepository, db_session: Callable[[], ContextManager[Session]]):
        self.repo = repo
        self.db_session = db_session

    def get_sensor(self, request: GetSensorRequest):
        with self.db_session() as session:
            sensor: Sensor = self.repo.find_sensor_by_measure_type(session=session, measure_type=request.measure_type)
            return sensor
        
    def get_all_sensor(self):
        with self.db_session() as session:
            return self.repo.get_all(session=session)
    