from dataclasses import dataclass
from worker.domain.model.value_object import PositionType
from worker.infra.repository import WorkerFlowStatusRepository
from worker.domain.model.aggregate import WorkerFlowStatus

from sqlalchemy.orm import Session

@dataclass
class CreateWorkerFlowStatusRequest:
    position: PositionType
    times_executed: int
    times_to_be_executed: int


class WorkerFlowStatusService:

    def __init__(self, repo: WorkerFlowStatusRepository):
        self.repo = repo
    
    def create_worker_flow_status(self, session: Session, request: CreateWorkerFlowStatusRequest) -> WorkerFlowStatus:
        obj = WorkerFlowStatus.create(
            times_executed=request.times_executed,
            times_to_be_executed=request.times_to_be_executed,
            position=request.position
        ) 
        self.repo.add(instance=obj, session=session)
        return obj
    
    def delete_worker_flow_status(self, session: Session):
        instance = self.repo.find_first(session)
        self.repo.delete(session, instance)

    