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
    GetStepDefinitionRequest,
    EventQueryUseCase
)
from worker.domain.model.aggregate import StepDefinition
from worker.domain.model.value_object import PositionType
from worker.domain.model.worker_service import WorkerService
from worker.application.services import WorkerFlowService

from shared_kernel.infra.container import AppContainer
from fastapi import WebSocket

router = APIRouter(prefix="/worker", tags=['worker'])

###############################################################
#                     STEP DEFINIION                          #
###############################################################

@router.get("/stepDefinition")
@inject
def get_steps_definition(
    query: StepDefinitionQueryUseCase = Depends(Provide[AppContainer.worker.query]),
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
    command: UpdateStepDefinitionCommand = Depends(Provide[AppContainer.worker.update_command]),
) -> None:
    command.execute(request=request)

@router.post("/stepDefinition")
@inject
def post_step_definition(
    request: CreateStepDefinitionRequest = Depends(),
    command: CreateStepDefinitionCommand = Depends(Provide[AppContainer.worker.create_command]),
) -> None:
    command.execute(request=request)

@router.delete("/stepDefinition")
@inject
def post_step_definition(
    request: GetStepDefinitionRequest = Depends(),
    command: CreateStepDefinitionCommand = Depends(Provide[AppContainer.worker.delete_command]),
) -> None:
    command.execute(request=request)

###############################################################
#                           FLOW                              #
###############################################################
worker_service = None
background_task = None
event_manager = EventManager()

@router.get("/start")
@inject
async def start(
    service: WorkerService = Depends(Provide[AppContainer.worker.worker_service]),
):
    global worker_service, background_task, event_manager
    if worker_service is None:
        worker_service = WorkerFlowService(
            worker_service=service,
            position=PositionType.FIRST,
            times_executed=1
        )
        event_manager = EventManager()
        event_manager.start()

        background_task = asyncio.create_task(worker_service.handle(event_manager))
        return {"status": "Task started"}
    elif worker_service.paused:
        worker_service.handle_resume()
        background_task = asyncio.create_task(worker_service.handle(event_manager))
        return {"status": "Task resumed"}

    return {"status": "Task already running"}

@router.get("/stop")
@inject
async def stop():
    global worker_service
    if worker_service:
        background_task.cancel()
        worker_service = None
        return {"status": "Task stopped"}
    else:
        return {"status": "Task not running yet"}

@router.get("/pause")
@inject
async def pause():
    global worker_service
    if worker_service:
        worker_service.handle_pause()
        return {"status": "Task paused"}
    else:
        return {"status": "Task not running yet"}

@router.get("/ws")
@inject
def websocket_endpoint(query: EventQueryUseCase = Depends(Provide[AppContainer.worker.event_query]),):
    response = query.get()
    if response:
        return response.description
