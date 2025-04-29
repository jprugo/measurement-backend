from dependency_injector import containers, providers

# Configuration
from configuration.infra.repository import ConfigurationRepository
from configuration.application.use_case import ConfigurationQueryUseCase

# Measurement
from measurement.application.use_cases.measurement_use_cases import DeviceMeasurementQueryUseCase, CreateMeasurementCommand
from measurement.infra.api.device_api_service import MeasurementDeviceApiService
from measurement.infra.api.device_repository import DeviceMeasureRepository
from measurement.infra.repository import MeasurementRepository
from measurement.domain.model.services.measurement_service import MeasurementService

# Alarming
from alarming.application.use_cases.alarm_definition_use_cases import AlarmDefinitionQueryUseCase
from alarming.application.use_cases.alarm_use_cases import CreateAlarmCommand
from alarming.domain.model.services import AlarmDefinitionService, AlarmService
from alarming.infra.repository import AlarmDefinitionRepository, AlarmRepository

# Worker
from worker.application.use_cases.worker_flow_status_use_case import WorkerFlowStatusQueryUseCase, WorkerFlowStatusUpdateCommand
from worker.application.use_cases.communicate_with_device import SendOfflineModeSignalCommand
from worker.infra.api.device_api_service import WorkerDeviceApiService

from worker.domain.model.services.worker_flow_status_service import WorkerFlowStatusService
from worker.infra.repository import StepDefinitionRepository, EventRepository, WorkerFlowStatusRepository

from worker.application.use_cases.step_definition_use_case import (
    StepDefinitionQueryUseCase,
    UpdateStepDefinitionCommand,
    CreateStepDefinitionCommand,
    DeleteStepDefinitionCommand,
    EventQueryUseCase, CreateEventCommand, DeleteEventCommand
)

from worker.domain.model.step_definition_service import StepDefinitionService
from worker.domain.model.services.worker_service import WorkerService

from shared_kernel.infra.database.connection import get_db_session


class WorkerContainer(containers.DeclarativeContainer):

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
    measurement_api_service = providers.Factory(
        MeasurementDeviceApiService,
        config_query= config_query
    )
    device_query = providers.Factory(
        DeviceMeasurementQueryUseCase,
        repo=device_repo,
        api_service=measurement_api_service,
    )

    measurement_repo = providers.Factory(MeasurementRepository)
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
    alarm_def_service = providers.Factory(
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

    # EVENT
    event_repository = providers.Factory(
        EventRepository,
    )
    event_query = providers.Factory(
        EventQueryUseCase,
        repo=event_repository,
        db_session=get_db_session,
    )
    event_command = providers.Factory(
        CreateEventCommand,
        db_session=get_db_session,
        repo=event_repository
    )
    delete_event_command = providers.Factory(
        DeleteEventCommand,
        db_session=get_db_session,
        repo=event_repository
    )

    # Service
    worker_service = providers.Factory(
        WorkerService,
        step_definition_query= query,
        measurement_command= measurement_command,
        measurement_query= device_query,
        alarm_def_query= alarm_def_query,
        alarm_command= alarm_command,
        event_command=event_command,
        device_api_service=measurement_api_service
    )

    # Worker Flow Status
    worker_flow_status_repo = providers.Factory(
        WorkerFlowStatusRepository,
    )

    worker_flow_status_query = providers.Factory(
        WorkerFlowStatusQueryUseCase,
        repo=worker_flow_status_repo,
        db_session=get_db_session
    )

    worker_flow_status_service = providers.Factory(
        WorkerFlowStatusService,
        repo=worker_flow_status_repo
    )

    worker_flow_status_command = providers.Factory(
        WorkerFlowStatusUpdateCommand,
        service=worker_flow_status_service,
        db_session=get_db_session
    )
    
    worker_api_service = providers.Factory(
        WorkerDeviceApiService,
        config_query= config_query,
        step_definition_query=query
    )
    send_offline_mode_signal_command = providers.Factory(
        SendOfflineModeSignalCommand,
        service=worker_api_service
    )
