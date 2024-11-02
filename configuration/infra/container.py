from dependency_injector import containers, providers

from configuration.infra.repository import ConfigurationRepository
from configuration.application.use_case import (
    ConfigurationQueryUseCase, 
    CreateConfigurationCommand, UpdateConfigurationCommand, DeleteConfigurationCommand
)
from configuration.domain.model.services import ConfigurationService

from shared_kernel.infra.database.connection import get_db_session


class ConfigurationContainer(containers.DeclarativeContainer):
    repo = providers.Factory(ConfigurationRepository)

    query = providers.Factory(
        ConfigurationQueryUseCase,
        repo=repo,
        db_session=get_db_session,
    )

    service = providers.Factory(
        ConfigurationService,
        repo=repo
    )

    create_command = providers.Factory(
        CreateConfigurationCommand,
        service= service,
        db_session=get_db_session,
    )

    update_command = providers.Factory(
        UpdateConfigurationCommand,
        service= service,
        db_session=get_db_session,
    )

    delete_command = providers.Factory(
        DeleteConfigurationCommand,
        service= service,
        db_session=get_db_session,
    )