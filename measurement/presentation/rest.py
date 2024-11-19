from typing import List, Optional
import csv

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from measurement.domain.model.services import GetMeasurementRequest, CreateMeasurementRequest
from measurement.domain.model.value_object import MeasureType, SensorType
from measurement.presentation.response import  MeasurementResponse, MeasurementSchema, LastMeasurementResponse, LastMeasurementSchema, get_last_measurement_id
from measurement.application.use_case import MeasurementQueryUseCase, CreateMeasurementCommand
from measurement.domain.model.aggregate import Measure

from shared_kernel.infra.container import AppContainer
from shared_kernel.infra import logger

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



@router.get("/export")
@inject
def export_measurements(
    measure_type: MeasureType,
    start_date: datetime,
    end_date: datetime,
    mountpoint: str,
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
    export_all_items(measures= measurements, mountpoint= mountpoint, measure_type= measure_type)
    return MeasurementResponse(
        detail="ok",
        result=[MeasurementSchema.from_orm(m) for m in measurements]
    )


def export_all_items(measures: List[Measure], mountpoint: str, measure_type: MeasureType):
        file_name = f'{mountpoint}/{measure_type.value}.csv'
        _write_to_csv(measures, file_name)


def _write_to_csv(data: List[Measure], filename: str):
    if data:
        data_dicts = [
            {key: value for key, value in obj.__dict__.items() if not key.startswith('_')}
            for obj in data
        ]
        
        fieldnames = data_dicts[0].keys() if data_dicts else []

        with open(filename, mode='w', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
            writer.writeheader()
            for row in data_dicts:
                writer.writerow(row)
    else:
        logger.logger.info("No hay datos para escribir en el archivo CSV.")
