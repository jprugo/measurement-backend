from dependency_injector import containers, providers

from option.infra.repository import OptionRepository
from option.application.use_case import OptionsQueryUseCase


class OptionContainer(containers.DeclarativeContainer):
    repo = providers.Factory(OptionRepository)

    query = providers.Factory(
        OptionsQueryUseCase,
        repo=repo,
    )
