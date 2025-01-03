from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from measurement.domain.model.services.measurement_service import CreateMeasurementRequest
from measurement.domain.model.services.sensor_service import CreateSensorRequest


from measurement.domain.model.value_object import MeasureType, SensorType
from measurement.domain.model.aggregate import Measure

from measurement.presentation.response import  (
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

from datetime import datetime

router = APIRouter(prefix="/measurement", tags=['measurement'])


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
        measure_type= measure_type,
        start_date= start_date,
        end_date= end_date,
        detail= detail
    )
    measurements: List[Measure] = measurement_query.get_measures(request=request)
    return MeasurementResponse(
        detail="ok",
        result=[MeasurementSchema.from_orm(m) for m in measurements]
    )


@router.get("/last")
@inject
def get_last_measurements(
    measurement_query: MeasurementQueryUseCase = Depends(Provide[AppContainer.measurement.query]),
) -> LastMeasurementResponse:
    measurements: List[Measure] = measurement_query.get_last_measures()
    return LastMeasurementResponse(
        detail="ok",
        result=[
            LastMeasurementSchema(
                id=get_last_measurement_id(measure_type=m.measure_type, detail=m.detail),
                value=m.value,
                created_at=m.created_at,
                measure_type=m.measure_type,
                detail=m.detail
            ) for m in measurements
        ]
    )


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
    
    return UnitResponse(
        detail="ok",
        result=[
            UnitSchema(
                name=u.name,
                value=u
            ) for u in MeasureType.get_units(measure_type)      
        ]
    )


@router.get("/sensorTypes")
@inject
def get_sensor_types(
) -> SensorTypeResponse:
    return SensorTypeResponse(
        detail="ok",
        result=list(SensorType)
    )


@router.get("/measureTypesBySensor")
@inject
def get_measure_types(
    sensor_type: SensorType
) -> MeasureTypeResponse:
    return MeasureTypeResponse(
        detail="ok",
        result=SensorType.get_measure_types(sensor_type)
    )


@router.get("/measureTypes")
@inject
def get_measure_types(
) -> MeasureTypeResponse:
    return MeasureTypeResponse(
        detail="ok",
        result=list(MeasureType)
    )


@router.post("/sensor")
@inject
def create_sensor(
    request: CreateSensorRequest = Depends(),
    command:  CreateSensorCommand = Depends(Provide[AppContainer.measurement.create_sensor_command]),
) -> None:
    command.execute(request=request)


@router.get("/sensor")
@inject
def get_sensor(
    measure_type: MeasureType,
    query:  SensorQueryUseCase = Depends(Provide[AppContainer.measurement.sensor_query]),
) -> SensorResponse:
    sensor= query.get_sensor(
        request=GetSensorRequest(
            measure_type=measure_type    
        )
    )
    schema = None
    if sensor:
        schema = SensorSchema(
            id=sensor.id,
            brand=sensor.brand,
            reference=sensor.reference,
            sensor_type=sensor.sensor_type,
            measurement_spec=[
                MeasurementSpecSchema(
                    measure_type=m.measure_type,
                    unit=m.unit,
                ) for m in sensor.measurement_specs
            ]
        )
    return SensorResponse(
        detail="ok",
        result=schema
    )


@router.get("/sensor/all")
@inject
def get_all_sensor(
    query:  SensorQueryUseCase = Depends(Provide[AppContainer.measurement.sensor_query]),
) -> SensorsResponse:
    sensors = query.get_all_sensor()
    return SensorsResponse(
        detail="ok",
        result=[
                SensorSchema(
                    id=s.id,
                    brand=s.brand,
                    reference=s.reference,
                    sensor_type=s.sensor_type,
                    measurement_spec=[
                        MeasurementSpecSchema(
                            measure_type=m.measure_type,
                            unit=m.unit,
                        ) for m in s.measurement_specs
                    ]
                ) for s in sensors
        ]
    )


@router.delete("/sensor")
@inject
def delete_sensor(
    request: GetSensorByIdRequest = Depends(),
    command: DeleteSensorCommand = Depends(Provide[AppContainer.measurement.delete_sensor_command]),
) -> None:
    command.execute(request=request)