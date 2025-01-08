import time
from typing import List, Optional
import asyncio
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from worker.application.use_cases.worker_flow_status_use_case import UpdateWorkerFlowStatusRequest, WorkerFlowStatusUpdateCommand, WorkerFlowStatusQueryUseCase
from worker.presentation.response import StepDefinitionResponse, StepDefinitionSchema
from worker.application.use_cases.step_definition_use_case import (
    StepDefinitionQueryUseCase,
    UpdateStepDefinitionCommand,
    UpdateStepDefinitionRequest,
    CreateStepDefinitionCommand,
    CreateStepDefinitionRequest,
    GetStepDefinitionRequest,
    EventQueryUseCase, CreateEventCommand, CreateEventCommandRequest
)
from worker.domain.model.aggregate import StepDefinition
from worker.domain.model.value_object import PositionType
from worker.domain.model.services.worker_service import WorkerService
from worker.application.services.worker_flow_service import WorkerFlowService

from shared_kernel.infra.container import AppContainer


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
worker_task: Optional[asyncio.Task] = None


@router.get("/start")
@inject
async def start(
    service: WorkerService = Depends(Provide[AppContainer.worker.worker_service]),
    worker_flow_status_query: WorkerFlowStatusQueryUseCase = Depends(Provide[AppContainer.worker.worker_flow_status_query]),
    worker_flow_status_command: WorkerFlowStatusUpdateCommand = Depends(Provide[AppContainer.worker.worker_flow_status_command]),
):
    global worker_service, worker_task

    if worker_service is None:
        worker_service = WorkerFlowService(
            worker_service=service,
            worker_flow_status_query=worker_flow_status_query,
            worker_flow_status_command=worker_flow_status_command
        )

        async def run_worker():
            while True:
                await worker_service.handle()
                time.sleep(10)
                
        worker_task = asyncio.create_task(run_worker())

        return {"status": "Task started"}
    else:
        return {"status": "Task resumed"}


@router.get("/stop")
@inject
async def stop(
    service: WorkerService = Depends(Provide[AppContainer.worker.worker_service]),
    worker_flow_status_command: WorkerFlowStatusUpdateCommand = Depends(Provide[AppContainer.worker.worker_flow_status_command]),
):
    global worker_service, worker_task

    if worker_service:
        # Cambiar el estado del worker a "detenido"
        worker_flow_status_command.execute(
            UpdateWorkerFlowStatusRequest(
                position=PositionType.FIRST,
                times_executed=1
            )
        )
        service.stop_measure()

        # Cancelar la tarea en segundo plano
        if worker_task:
            worker_task.cancel()
            try:
                await worker_task
            except asyncio.CancelledError:
                pass

        worker_service = None
        worker_task = None

        return {"status": "Task stopped"}
    else:
        return {"status": "Task not running yet"}
    

@router.get("/pause")
@inject
async def stop(
    service: WorkerService = Depends(Provide[AppContainer.worker.worker_service]),
):
    global worker_service, worker_task

    if worker_service:
        service.stop_measure()

        if worker_task:
            worker_task.cancel()
            try:
                await worker_task
            except asyncio.CancelledError:
                pass

        worker_service = None
        worker_task = None

        return {"status": "Task paused"}
    else:
        return {"status": "Task not running yet"}


@router.get("/ws")
@inject
def websocket_endpoint(query: EventQueryUseCase = Depends(Provide[AppContainer.worker.event_query])):
    try:
        response = query.get()
        return response
    except Exception:
        return None


@router.post("/ws")
@inject
def websocket_endpoint(title: str, description: str, command: CreateEventCommand = Depends(Provide[AppContainer.worker.event_command])):
    command.execute(
        request=CreateEventCommandRequest(
            title=title,
            description=description
        )
    )
