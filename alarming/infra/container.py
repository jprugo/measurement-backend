from dependency_injector import containers, providers

from alarming.application.use_case import (
    AlarmDefinitionQueryUseCase, AlarmQueryUseCase,
    # Command
    CreateAlarmDefinitionCommand, CreateAlarmCommand,
    UpdateAlarmDefinitionCommand, DeleteAlarmDefinitionCommand
)

from alarming.infra.repository import AlarmDefinitionRepository, AlarmRepository
from alarming.domain.model.services import AlarmDefinitionService, AlarmService

from shared_kernel.infra.database.connection import get_db_session

class AlarmContainer(containers.DeclarativeContainer):

    ###############################################################
    #                            ALARM                            #
    ###############################################################
    
    alarms_repo = providers.Factory(AlarmRepository)
    
    alarm_query = providers.Factory(
        AlarmQueryUseCase,
        repo=alarms_repo,
        db_session=get_db_session,
    )

    alarm_service = providers.Factory(
        AlarmService,
        repo=alarms_repo
    )

    create_alarm_command = providers.Factory(
        CreateAlarmCommand,
        service=alarm_service,
        db_session=get_db_session
    )

    ###############################################################
    #                      ALARM DEFINITION                       #
    ###############################################################

    alarms_definition_repo = providers.Factory(AlarmDefinitionRepository)

    alarm_definition_query = providers.Factory(
        AlarmDefinitionQueryUseCase,
        repo=alarms_definition_repo,
        db_session=get_db_session,
    )

    alarm_definition_service = providers.Factory(
        AlarmDefinitionService,
        repo=alarms_definition_repo
    )

    create_alarm_definition_command = providers.Factory(
        CreateAlarmDefinitionCommand,
        service=alarm_definition_service,
        db_session=get_db_session
    )

    update_alarm_definition_command = providers.Factory(
        UpdateAlarmDefinitionCommand,
        service=alarm_definition_service,
        db_session=get_db_session
    )

    delete_alarm_definition_command = providers.Factory(
        DeleteAlarmDefinitionCommand,
        service=alarm_definition_service,
        db_session=get_db_session
    )