from dependency_injector import containers, providers

from measurement.infra.repository import MeasurementRepository
from measurement.application.use_case import MeasurementQueryUseCase, CreateMeasurementCommand
from measurement.domain.model.services import MeasurementService
from shared_kernel.infra.database.connection import get_db_session


class MeasurementContainer(containers.DeclarativeContainer):
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