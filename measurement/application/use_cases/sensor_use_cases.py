from typing import Callable, ContextManager

from sqlalchemy.orm import Session

from measurement.domain.model.aggregate import Measure, Sensor
from measurement.domain.model.value_object import MeasureType
from measurement.infra.repository import SensorRepository
from measurement.domain.model.services.sensor_service import (
    CreateSensorRequest,
    SensorService
)

from pydantic import BaseModel


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
    