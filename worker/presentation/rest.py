import os
import sys
from typing import List
import asyncio

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from shared_kernel.infra.event_manager import EventManager
from worker.presentation.response import StepDefinitionResponse, StepDefinitionSchema
from worker.application.step_definition_use_case import (
    StepDefinitionQueryUseCase,
    UpdateStepDefinitionCommand,
    UpdateStepDefinitionRequest,
    CreateStepDefinitionCommand,
    CreateStepDefinitionRequest,
    GetStepDefinitionRequest
)
from worker.domain.model.aggregate import StepDefinition
from worker.domain.model.value_object import PositionType
from worker.domain.model.worker_service import WorkerService

from shared_kernel.infra.container import AppContainer

router = APIRouter(prefix="/worker", tags=['worker'])

event_manager = EventManager()
current_background_task = None

###############################################################
#                     STEP DEFINIION                          #
###############################################################

@router.get("/stepDefinition")
@inject
def get_steps_definition(
    query: StepDefinitionQueryUseCase = Depends(Provide[AppContainer.step_definition.query]),
) -> StepDefinitionResponse:
    data: List[StepDefinition] = query.get_all_step_definition()
    return StepDefinitionResponse(
        detail="ok",
        result=[StepDefinitionSchema.from_orm(c) for c in data]
    )

@router.put("/stepDefinition")
@inject
def update_step_definition(
    request: UpdateStepDefinitionRequest = Depends(),
    command: UpdateStepDefinitionCommand = Depends(Provide[AppContainer.step_definition.update_command]),
) -> None:
    command.execute(request=request)

@router.post("/stepDefinition")
@inject
def post_step_definition(
    request: CreateStepDefinitionRequest = Depends(),
    command: CreateStepDefinitionCommand = Depends(Provide[AppContainer.step_definition.create_command]),
) -> None:
    command.execute(request=request)

@router.delete("/stepDefinition")
@inject
def post_step_definition(
    request: GetStepDefinitionRequest = Depends(),
    command: CreateStepDefinitionCommand = Depends(Provide[AppContainer.step_definition.delete_command]),
) -> None:
    command.execute(request=request)

###############################################################
#                           FLOW                              #
###############################################################

@router.get("/start")
@inject
async def start(
    service: WorkerService = Depends(Provide[AppContainer.step_definition.worker_service]),
):
    global current_background_task, event_manager
    if current_background_task is None:
        event_manager = EventManager()
        event_manager.start()
        current_background_task = asyncio.create_task(run_background_task(service.handle, position=PositionType.FIRST, event_manager=event_manager))
        return {"status": "Task started"}
    return {"status": "Task already running"}

@router.get("/stop")
@inject
async def stop(
     service: WorkerService = Depends(Provide[AppContainer.step_definition.worker_service]),
):
    global current_background_task, event_manager
    if current_background_task:
        # Send stop signal
        service.stop_measure()
        # Event manager stop
        event_manager.stop()
        current_background_task.cancel()
        try:
            await current_background_task
        except asyncio.CancelledError:
            pass
        current_background_task = None
        event_manager = None

    return {"status": "Task stopped"}

async def run_background_task(callback, **args):    
    event_manager.subscribe(lambda __, **kwargs: asyncio.create_task(callback(**kwargs)))
    event_manager.publish("Loop", **args)
