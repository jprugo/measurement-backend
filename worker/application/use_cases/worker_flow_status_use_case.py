from typing import Callable, ContextManager
from sqlalchemy.orm import Session
from worker.domain.model.aggregate import WorkerFlowStatus
from worker.infra.repository import WorkerFlowStatusRepository
from worker.domain.model.services.worker_flow_status_service import UpdateWorkerFlowStatusRequest, WorkerFlowStatusService


class WorkerFlowStatusQueryUseCase:
    def __init__(self, repo: WorkerFlowStatusRepository, db_session: Callable[[], ContextManager[Session]]):
        self.repo = repo
        self.db_session = db_session

    def get_worker_flow_status(self) -> WorkerFlowStatus:
        with self.db_session() as session:
            return self.repo.find_first(session=session)


class WorkerFlowStatusUpdateCommand:
    def __init__(self, service: WorkerFlowStatusService, db_session: Callable[[], ContextManager[Session]]):
        self.service = service
        self.db_session = db_session

    def execute(self, request: UpdateWorkerFlowStatusRequest) -> WorkerFlowStatus:
        with self.db_session() as session:
            step_definition = self.service.update_worker_flow_status(session=session, request=request)
            session.commit()
            return step_definition



