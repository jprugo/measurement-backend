from dependency_injector import containers, providers

from measurement.infra.repository import MeasurementRepository, SensorRepository
from measurement.application.use_cases.measurement_use_cases import (
    MeasurementQueryUseCase,
    CreateMeasurementCommand,
)

from measurement.application.use_cases.sensor_use_cases import (
    SensorQueryUseCase, DeleteSensorCommand, CreateSensorCommand
)

from measurement.domain.model.services.measurement_service import MeasurementService
from measurement.domain.model.services.sensor_service import SensorService

from shared_kernel.infra.database.connection import get_db_session


class MeasurementContainer(containers.DeclarativeContainer):
    # Measurement
    repo = providers.Factory(MeasurementRepository)

    query = providers.Factory(
        MeasurementQueryUseCase,
        repo=repo,
        db_session=get_db_session,
    )

    service = providers.Factory(
        MeasurementService,
        repo=repo,
    )

    create_measurement_command = providers.Factory(
        CreateMeasurementCommand,
        service=service,
        db_session=get_db_session,
    )

    # Sensor
    sensor_repo = providers.Factory(SensorRepository)

    sensor_service = providers.Factory(
        SensorService,
        repo=sensor_repo
    )

    sensor_query = providers.Factory(
        SensorQueryUseCase,
        repo=sensor_repo,
        db_session=get_db_session,
    )

    delete_sensor_command = providers.Factory(
        DeleteSensorCommand,
        service=sensor_service,
        db_session=get_db_session,
    )

    create_sensor_command = providers.Factory(
        CreateSensorCommand,
        service=sensor_service,
        db_session=get_db_session,
    )