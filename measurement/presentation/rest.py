from typing import List, Optional
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from datetime import datetime

from measurement.domain.model.services.measurement_service import CreateMeasurementRequest
from measurement.domain.model.services.sensor_service import CreateSensorRequest
from measurement.domain.model.value_object import MeasureType, SensorType
from measurement.domain.model.aggregate import Measure
from measurement.presentation.response import (
    MeasurementResponse, MeasurementSchema,
    LastMeasurementResponse, LastMeasurementSchema,
    SensorResponse, SensorSchema, MeasurementSpecSchema, 
    SensorTypeResponse, SensorsResponse, MeasureTypeResponse,
    UnitResponse, UnitSchema, get_last_measurement_id
)
from measurement.application.use_cases.measurement_use_cases import (
    MeasurementQueryUseCase, GetMeasurementRequest,
    CreateMeasurementCommand,
)
from measurement.application.use_cases.sensor_use_cases import (
    CreateSensorCommand, GetSensorByIdRequest, SensorQueryUseCase, GetSensorRequest, DeleteSensorCommand
)
from shared_kernel.infra.container import AppContainer


router = APIRouter(prefix="/measurement", tags=['measurement'])

def map_measurements_to_schema(measurements: List[Measure]) -> List[MeasurementSchema]:
    return [MeasurementSchema.from_orm(m) for m in measurements]

def map_sensor_to_schema(sensor) -> SensorSchema:
    return SensorSchema(
        id=sensor.id,
        brand=sensor.brand,
        reference=sensor.reference,
        sensor_type=sensor.sensor_type,
        measurement_spec=[
            MeasurementSpecSchema(measure_type=m.measure_type, unit=m.unit) 
            for m in sensor.measurement_specs
        ]
    )

def map_unit_schemas(units) -> List[UnitSchema]:
    return [UnitSchema(name=u.name, value=u) for u in units]


@router.get("/")
@inject
def get_measurements(
    measure_type: MeasureType,
    start_date: datetime,
    end_date: datetime,
    detail: Optional[str] = None,
    measurement_query: MeasurementQueryUseCase = Depends(Provide[AppContainer.measurement.query]),
) -> MeasurementResponse:
    request = GetMeasurementRequest(
        measure_type=measure_type,
        start_date=start_date,
        end_date=end_date,
        detail=detail
    )
    measurements: List[Measure] = measurement_query.get_measures(request=request)
    return MeasurementResponse(
        detail="ok",
        result=map_measurements_to_schema(measurements)
    )


@router.get("/last")
@inject
def get_last_measurements(
    measurement_query: MeasurementQueryUseCase = Depends(Provide[AppContainer.measurement.query]),
    sensor_query: SensorQueryUseCase = Depends(Provide[AppContainer.measurement.sensor_query]),
) -> LastMeasurementResponse:
    measurements: List[Measure] = measurement_query.get_last_measures()
    response_list = []
    
    for m in measurements:
        sensor_response = sensor_query.get_sensor(
            GetSensorRequest(measure_type=m.measure_type)
        )
        unit = None
        if sensor_response:
            unit = next(
                (s.unit for s in sensor_response.measurement_specs if s.measure_type == m.measure_type), 
                None
            )

        response_list.append(LastMeasurementSchema(
            id=get_last_measurement_id(measure_type=m.measure_type, detail=m.detail),
            value=m.value,
            created_at=m.created_at,
            measure_type=m.measure_type,
            detail=m.detail,
            unit=unit
        ))

    return LastMeasurementResponse(detail="ok", result=response_list)


@router.post("/")
@inject
def post_measurement(
    request: CreateMeasurementRequest = Depends(),
    command: CreateMeasurementCommand = Depends(Provide[AppContainer.measurement.create_measurement_command]),
) -> None:
    command.execute(request=request)


@router.get("/units")
@inject
def get_units(
    measure_type: MeasureType,
) -> UnitResponse:
    units = MeasureType.get_units(measure_type)
    return UnitResponse(
        detail="ok",
        result=map_unit_schemas(units)
    )


@router.get("/unitsConfiguredByMeasureType")
@inject
def get_units_configured_by_measure_type(
    measure_type: MeasureType,
    query: SensorQueryUseCase = Depends(Provide[AppContainer.measurement.sensor_query]),
) -> UnitResponse:
    sensor = query.get_sensor(
        request=GetSensorRequest(measure_type=measure_type)
    )
    if sensor:
        measurement_specs = [
            MeasurementSpecSchema(measure_type=m.measure_type, unit=m.unit)
            for m in sensor.measurement_specs if m.measure_type == measure_type
        ]
        units = [UnitSchema(name=m.unit.name, value=m.unit.value) for m in measurement_specs]
        return UnitResponse(detail="ok", result=units)

    return UnitResponse(detail="ok", result=[])


@router.get("/sensorTypes")
@inject
def get_sensor_types() -> SensorTypeResponse:
    return SensorTypeResponse(detail="ok", result=list(SensorType))


@router.get("/measureTypesBySensor")
@inject
def get_measure_types_by_sensor(sensor_type: SensorType) -> MeasureTypeResponse:
    return MeasureTypeResponse(detail="ok", result=SensorType.get_measure_types(sensor_type))


@router.get("/measureTypes")
@inject
def get_measure_types() -> MeasureTypeResponse:
    return MeasureTypeResponse(detail="ok", result=list(MeasureType))


@router.post("/sensor")
@inject
def create_sensor(
    request: CreateSensorRequest = Depends(),
    command: CreateSensorCommand = Depends(Provide[AppContainer.measurement.create_sensor_command]),
) -> None:
    command.execute(request=request)


@router.get("/sensor")
@inject
def get_sensor(
    measure_type: MeasureType,
    query: SensorQueryUseCase = Depends(Provide[AppContainer.measurement.sensor_query]),
) -> SensorResponse:
    sensor = query.get_sensor(
        request=GetSensorRequest(measure_type=measure_type)
    )
    schema = map_sensor_to_schema(sensor) if sensor else None
    return SensorResponse(detail="ok", result=schema)


@router.get("/sensor/all")
@inject
def get_all_sensors(
    query: SensorQueryUseCase = Depends(Provide[AppContainer.measurement.sensor_query]),
) -> SensorsResponse:
    sensors = query.get_all_sensor()
    return SensorsResponse(
        detail="ok",
        result=[map_sensor_to_schema(s) for s in sensors]
    )


@router.delete("/sensor")
@inject
def delete_sensor(
    request: GetSensorByIdRequest = Depends(),
    command: DeleteSensorCommand = Depends(Provide[AppContainer.measurement.delete_sensor_command]),
) -> None:
    command.execute(request=request)
