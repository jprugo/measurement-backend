import random
from typing import Any
from typing import List, Optional
from datetime import datetime
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from measurement.domain.model.services.measurement_service import CreateMeasurementRequest
from measurement.domain.model.services.sensor_service import CreateSensorRequest
from measurement.domain.model.value_object import MeasureType, SensorType, Unit
from measurement.domain.model.aggregate import Measure, Sensor
from measurement.presentation.response import (
    MeasurementResponse, MeasurementResponse2, MeasurementSchema,
    LastMeasurementResponse, LastMeasurementSchema,
    SensorResponse, SensorSchema, MeasurementSpecSchema,
    SensorTypeResponse, SensorsResponse, MeasureTypeResponse,
    UnitResponse, UnitSchema, get_last_measurement_id
)
from measurement.application.use_cases.measurement_use_cases import (
    MeasurementQueryUseCase, GetMeasurementRequest, GetMeasurementByTimeDeltaRequest,
    CreateMeasurementCommand,
)
from measurement.application.use_cases.sensor_use_cases import (
    CreateSensorCommand, GetSensorByIdRequest, SensorQueryUseCase, GetSensorRequest, DeleteSensorCommand
)
from shared_kernel.infra.container import AppContainer
from pydantic import BaseModel

router = APIRouter(prefix="/measurement", tags=['measurement'])

# Mapper functions


def map_measurements_to_schema(measurements: List[Measure], unit: UnitSchema) -> List[MeasurementSchema]:
    measurements_schema = [
        MeasurementSchema.from_orm(m)
        for m in measurements
    ]

    for measurement in measurements_schema:
        measurement.unit = None if unit is None else unit.value

    return measurements_schema


def map_sensor_to_schema(sensor: Sensor) -> SensorSchema:
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


def map_unit_schemas(units: List[Unit]) -> List[UnitSchema]:
    return [UnitSchema(name=u.name, value=u) for u in units]

# API routes


@router.get("/getByTimeDelta")
@inject
def get_measurements(
    measure_type: MeasureType,
    minutes: int,
    detail: Optional[str] = None,
    measurement_query: MeasurementQueryUseCase = Depends(
        Provide[AppContainer.measurement.query]),
) -> MeasurementResponse2:
    request = GetMeasurementByTimeDeltaRequest(
        measure_type=measure_type,
        minutes_ago=minutes,
        detail=detail
    )
    measurement = measurement_query.get_measure_by_time_delta(request=request)
    return MeasurementResponse2(
        detail="ok",
        result=MeasurementSchema.from_orm(
            measurement) if measurement is not None else None
    )


@router.get("/")
@inject
def get_measurements(
    measure_type: MeasureType,
    start_date: datetime,
    end_date: datetime,
    detail: Optional[str] = None,
    measurement_query: MeasurementQueryUseCase = Depends(
        Provide[AppContainer.measurement.query]),
    sensor_query: SensorQueryUseCase = Depends(
        Provide[AppContainer.measurement.sensor_query]),
) -> MeasurementResponse:
    request = GetMeasurementRequest(
        measure_type=measure_type,
        start_date=start_date,
        end_date=end_date,
        detail=detail
    )
    sensor_response = sensor_query.get_sensor(
        GetSensorRequest(measure_type=measure_type)
    )
    unit = next(
        (s.unit for s in sensor_response.measurement_specs if s.measure_type == measure_type),
        None
    ) if sensor_response else None
    unit_schema = None
    if unit:
        unit_schema = UnitSchema(
            name=unit,
            value=unit
        )
    measurements = measurement_query.get_measures(request=request)
    return MeasurementResponse(
        detail="ok",
        result=map_measurements_to_schema(measurements, unit=unit_schema)
    )


@router.get("/last")
@inject
def get_last_measurements(
    measurement_query: MeasurementQueryUseCase = Depends(
        Provide[AppContainer.measurement.query]),
    sensor_query: SensorQueryUseCase = Depends(
        Provide[AppContainer.measurement.sensor_query]),
) -> LastMeasurementResponse:
    measurements = measurement_query.get_last_measures()
    response_list = []

    for m in measurements:
        sensor_response = sensor_query.get_sensor(
            GetSensorRequest(measure_type=m.measure_type)
        )
        unit = next(
            (s.unit for s in sensor_response.measurement_specs if s.measure_type == m.measure_type),
            None
        ) if sensor_response else None

        response_list.append(LastMeasurementSchema(
            id=get_last_measurement_id(
                measure_type=m.measure_type, detail=m.detail),
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
    command: CreateMeasurementCommand = Depends(
        Provide[AppContainer.measurement.create_measurement_command]),
) -> None:
    command.execute(request=request)


class MeasuresListSchema(BaseModel):
    measures: List[CreateMeasurementRequest]


@router.post("/list")
@inject
def post_measurement_list(
    request: MeasuresListSchema,
    command: CreateMeasurementCommand = Depends(
        Provide[AppContainer.measurement.create_measurement_command]),
) -> None:
    for measure in request.measures:
        command.execute(request=measure)


@router.get("/units")
@inject
def get_units(measure_type: MeasureType) -> UnitResponse:
    units = MeasureType.get_units(measure_type)
    return UnitResponse(
        detail="ok",
        result=map_unit_schemas(units)
    )


@router.get("/unitsConfiguredByMeasureType")
@inject
def get_units_configured_by_measure_type(
    measure_type: MeasureType,
    query: SensorQueryUseCase = Depends(
        Provide[AppContainer.measurement.sensor_query]),
) -> UnitResponse:
    try:
        units = get_unit_configured_by_measure_type(query, measure_type)
        return UnitResponse(detail="ok", result=units)
    except Exception:
        return UnitResponse(detail="error", result=[])


def get_unit_configured_by_measure_type(query: SensorQueryUseCase, measure_type: MeasureType) -> List[UnitSchema]:
    sensor = query.get_sensor(GetSensorRequest(measure_type=measure_type))
    if not sensor:
        raise Exception(f"Sensor for {measure_type} not configured.")
    measurement_specs = [
        MeasurementSpecSchema(measure_type=m.measure_type, unit=m.unit)
        for m in sensor.measurement_specs if m.measure_type == measure_type
    ]
    return [UnitSchema(name=m.unit.name, value=m.unit.value) for m in measurement_specs]


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
    command: CreateSensorCommand = Depends(
        Provide[AppContainer.measurement.create_sensor_command]),
) -> None:
    command.execute(request=request)


@router.get("/sensor")
@inject
def get_sensor(
    measure_type: MeasureType,
    query: SensorQueryUseCase = Depends(
        Provide[AppContainer.measurement.sensor_query]),
) -> SensorResponse:
    sensor = query.get_sensor(GetSensorRequest(measure_type=measure_type))
    schema = map_sensor_to_schema(sensor) if sensor else None
    return SensorResponse(detail="ok", result=schema)


@router.get("/sensor/all")
@inject
def get_all_sensors(
    query: SensorQueryUseCase = Depends(
        Provide[AppContainer.measurement.sensor_query]),
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
    command: DeleteSensorCommand = Depends(
        Provide[AppContainer.measurement.delete_sensor_command]),
) -> None:
    command.execute(request=request)


# Test

BATTERY_VALUE = 91


@router.get("/ISO")
def mock_iso(
) -> dict[str, Any]:
    return {
        "measures": [
            {
                # ISOLATION: Valor aleatorio entre 20.0 y 30.0
                "value": round(random.uniform(20.0, 30.0), 2),
                "measure_type": "ISOLATION",
                "detail": ""
            },
            {
                # ISOLATION_VOLTAGE: Valor aleatorio entre 40.0 y 50.0
                "value": round(random.uniform(40.0, 50.0), 2),
                "measure_type": "ISOLATION_VOLTAGE",
                "detail": ""
            },
            {
                # LEAKEGE_CURRENT: Valor aleatorio entre 10.0 y 15.0
                "value": round(random.uniform(10.0, 15.0), 2),
                "measure_type": "LEAKEGE_CURRENT",
                "detail": ""
            },
            {
                # BATTERY: Valor constante
                "value": BATTERY_VALUE,
                "measure_type": "BATTERY",
                "detail": ""
            }
        ]
    }


@router.get("/RES")
def mock_res(
) -> dict[str, Any]:
    base_res = random.uniform(1.0, 10.0)

    return {
        "measures": [
            {
                # RESISTANCE A-B: Valor aleatorio alrededor de 'base_res' (ej: +/- 3)
                "value": round(random.uniform(base_res - 3, base_res + 3), 2),
                "measure_type": "RESISTANCE",
                "detail": "A-B"
            },
            {
                # RESISTANCE B-C: Valor aleatorio alrededor de 'base_res' (ej: +/- 3)
                "value": round(random.uniform(base_res - 3, base_res + 3), 2),
                "measure_type": "RESISTANCE",
                "detail": "B-C"
            },
            {
                # RESISTANCE C-A: Valor aleatorio alrededor de 'base_res' (ej: +/- 3)
                "value": round(random.uniform(base_res - 3, base_res + 3), 2),
                "measure_type": "RESISTANCE",
                "detail": "C-A"
            },
            {
                # BATTERY: Valor constante
                "value": BATTERY_VALUE,
                "measure_type": "BATTERY",
                "detail": ""
            }
        ]
    }


@router.get("/WELL")
def mock_well(
) -> dict[str, Any]:
    return {
        "measures": [
            {
                # PRESSURE Pi: Valor aleatorio entre 20.0 y 30.0
                "value": round(random.uniform(400.0, 600.0), 2),
                "measure_type": "PRESSURE",
                "detail": "Pi"
            },
            {
                # PRESSURE Pd: Valor aleatorio entre 40.0 y 50.0
                "value": round(random.uniform(400.0, 600.0), 2),
                "measure_type": "PRESSURE",
                "detail": "Pd"
            },
            {
                # VIBRATION X: Valor aleatorio entre 10.0 y 15.0
                "value": round(random.uniform(10.0, 15.0), 2),
                "measure_type": "VIBRATION",
                "detail": "X"
            },
            {
                # VIBRATION Z: Valor aleatorio entre 10.0 y 15.0
                "value": round(random.uniform(10.0, 15.0), 2),
                "measure_type": "VIBRATION",
                "detail": "Z"
            },
            {
                # TEMPERATURE Ti: Valor aleatorio entre 10.0 y 20.0
                "value": round(random.uniform(90.0, 250.0), 2),
                "measure_type": "TEMPERATURE",
                "detail": "Ti"
            },
            {
                # TEMPERATURE Tm: Valor aleatorio entre 20.0 y 30.0
                "value": round(random.uniform(90.0, 250.0), 2),
                "measure_type": "TEMPERATURE",
                "detail": "Tm"
            },
            {
                # TOOL_CURRENT: Valor aleatorio entre 10.0 y 15.0
                "value": round(random.uniform(10.0, 15.0), 2),
                "measure_type": "TOOL_CURRENT",
                "detail": ""
            },
            {
                # TOOL_VOLTAGE: Valor aleatorio entre 10.0 y 15.0
                "value": round(random.uniform(10.0, 15.0), 2),
                "measure_type": "TOOL_VOLTAGE",
                "detail": "Tm"
            }
        ]
    }


@router.get("/stop")
def mock_well(
) -> None:
    return None
