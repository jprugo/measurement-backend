from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from configuration.presentation.response import  (
    ConfigurationResponse,
    ConfigurationSchema,
    SetUpResponse
)
from configuration.application.use_case import (
    ConfigurationQueryUseCase,
    # Command
    CreateConfigurationCommand,
    UpdateConfigurationCommand,
    DeleteConfigurationCommand,
    # Request
    CreateConfigurationRequest,
    UpdateConfigurationRequest,
    GetConfigurationRequest,
    GetConfigurationByIdRequest
)
from configuration.domain.model.aggregate import Configuration
from shared_kernel.infra.container import AppContainer
import pygame


router = APIRouter(prefix="/configuration", tags=['configuration'])


@router.get("/")
@inject
def get_configuration(
    configuration_query: ConfigurationQueryUseCase = Depends(Provide[AppContainer.configuration.query]),
) -> ConfigurationResponse:
    configs: List[Configuration] = configuration_query.get_configurations()
    return ConfigurationResponse(
        detail="ok",
        result=[ConfigurationSchema.from_orm(c) for c in configs]
    )

@router.post("/")
@inject
def post_configuration(
    request: CreateConfigurationRequest = Depends(),
    command: CreateConfigurationCommand = Depends(Provide[AppContainer.configuration.create_command]),
) -> None:
    command.execute(request=request)
    

@router.put("/")
@inject
def update_configuration(
    request: UpdateConfigurationRequest = Depends(),
    command: UpdateConfigurationCommand = Depends(Provide[AppContainer.configuration.update_command]),
) -> None:
    command.execute(request=request)


@router.delete("/")
@inject
def delete_configuration(
    request: GetConfigurationByIdRequest = Depends(),
    command: DeleteConfigurationCommand = Depends(Provide[AppContainer.configuration.delete_command]),
) -> None:
    command.execute(request=request)


@router.put("/setup")
@inject
def setup(
    configuration_query: ConfigurationQueryUseCase = Depends(Provide[AppContainer.configuration.query]),
) -> SetUpResponse:
    return SetUpResponse(
        detail= "ok",
        voltage = configuration_query.get_configuration(request = GetConfigurationRequest(name='isolationVoltage'))[0].value
    )


@router.get("/emitSound")
@inject
def setup(
    configuration_query: ConfigurationQueryUseCase = Depends(Provide[AppContainer.configuration.query]),
):
    sound_path = configuration_query.get_configuration(request = GetConfigurationRequest(name='soundPath'))
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
