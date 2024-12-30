from typing import List

from sqlalchemy.orm import Session

from measurement.domain.model.aggregate import  Sensor, MeasurementSpec
from measurement.domain.model.value_object import MeasureType, Unit, SensorType
from measurement.infra.repository import  SensorRepository
from pydantic import BaseModel


class CreateMeasurementSpecRequest(BaseModel):
    measure_type: MeasureType
    unit: Unit


class CreateSensorRequest(BaseModel):
    brand: str
    reference: str 
    sensor_type: SensorType
    measurement_specs: List[CreateMeasurementSpecRequest]


class GetSensorByIdRequest(BaseModel):
    id: int


class SensorService:
    def __init__(self, repo: SensorRepository):
        self.repo = repo

    def create_sensor(self, session: Session, request: CreateSensorRequest) -> Sensor:
        sensor = self.repo.find_sensor_by_measure_types(session=session, measure_types=[
            t.measure_type for t in request.measurement_specs
        ])
        
        if not sensor:
            sensor = Sensor.create(
                brand=request.brand,
                reference=request.reference,
                sensor_type=request.sensor_type,
                measure_sensor_details=[
                    MeasurementSpec.create(
                        measure_type=m.measure_type,
                        unit=m.unit
                    ) for m in request.measurement_specs
                ]
            )
            sensor = self.repo.add(instance=sensor, session=session)
        
        return sensor


    def delete_sensor(self, session: Session, request: GetSensorByIdRequest) -> None:
        sensor = self.repo.get_by_id(session=session, entity_id=request.id)
        if sensor:
            self.repo.delete(instance=sensor, session=session)