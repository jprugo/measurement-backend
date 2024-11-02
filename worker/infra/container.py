from dependency_injector import containers, providers

from configuration.infra.repository import ConfigurationRepository
from configuration.application.use_case import ConfigurationQueryUseCase

from measurement.application.use_case import DeviceMeasurementQueryUseCase, CreateMeasurementCommand
from measurement.infra.api.device_api_service import DeviceApiService
from measurement.infra.api.device_repository import DeviceMeasureRepository
from measurement.infra.repository import MeasurementRepository
from measurement.domain.model.services import MeasurementService

from alarming.application.use_case import AlarmDefinitionQueryUseCase, CreateAlarmCommand
from alarming.domain.model.services import AlarmDefinitionService, AlarmService
from alarming.infra.repository import AlarmDefinitionRepository, AlarmRepository

from worker.infra.repository import StepDefinitionRepository
from worker.application.step_definition_use_case import StepDefinitionQueryUseCase, UpdateStepDefinitionCommand, CreateStepDefinitionCommand, DeleteStepDefinitionCommand
from worker.domain.model.step_definition_service import StepDefinitionService
from worker.domain.model.worker_service import WorkerService

from shared_kernel.infra.database.connection import get_db_session


class StepDefinitionContainer(containers.DeclarativeContainer):

    # Configuration
    config_repo = providers.Factory(ConfigurationRepository)
    config_query = providers.Factory(
        ConfigurationQueryUseCase,
        repo=config_repo,
        db_session=get_db_session,
    )

    # Step definition
    repo = providers.Factory(StepDefinitionRepository)
    
    query = providers.Factory(
        StepDefinitionQueryUseCase,
        repo=repo,
        db_session=get_db_session,
    )

    service = providers.Factory(
        StepDefinitionService,
        repo=repo
    )

    update_command = providers.Factory(
        UpdateStepDefinitionCommand,
        service=service,
        db_session=get_db_session,
    )

    create_command = providers.Factory(
        CreateStepDefinitionCommand,
        service=service,
        db_session=get_db_session,
    )

    delete_command = providers.Factory(
        DeleteStepDefinitionCommand,
        service=service,
        db_session=get_db_session,
    )

    # DEVICE MEASUREMENT QUERY
    device_repo = providers.Factory(DeviceMeasureRepository)
    measurement_repo = providers.Factory(MeasurementRepository)
    api_service = providers.Factory(
        DeviceApiService,
        config_query= config_query
    )
    
    device_query = providers.Factory(
        DeviceMeasurementQueryUseCase,
        repo=device_repo,
        api_service=api_service,
    )

    measurement_service = providers.Factory(
        MeasurementService,
        repo=measurement_repo,
    )

    measurement_command = providers.Factory(
        CreateMeasurementCommand,
        service=measurement_service,
        db_session=get_db_session,
    )

    # ALARM DEF
    alarm_def_repo = providers.Factory(AlarmDefinitionRepository)
    
    alarm_def_query = providers.Factory(
        AlarmDefinitionQueryUseCase,
        repo=alarm_def_repo,
        db_session=get_db_session,
    )

    alarm__service = providers.Factory(
        AlarmDefinitionService,
        repo=alarm_def_repo
    )

    # AlARM
    alarm_repo = providers.Factory(AlarmRepository)

    alarm_service = providers.Factory(
        AlarmService,
        repo=alarm_repo
    )

    alarm_command = providers.Factory(
        CreateAlarmCommand,
        service=alarm_service,
        db_session=get_db_session,
    )

    worker_service = providers.Factory(
        WorkerService,
        step_definition_query= query,
        measurement_command= measurement_command,
        measurement_query= device_query,
        alarm_def_query= alarm_def_query,
        alarm_command= alarm_command,
        device_api_service=api_service
    )

   