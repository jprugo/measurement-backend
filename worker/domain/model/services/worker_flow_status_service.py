from dataclasses import dataclass
from worker.domain.model.value_object import PositionType
from worker.infra.repository import WorkerFlowStatusRepository
from worker.domain.model.aggregate import WorkerFlowStatus

from sqlalchemy.orm import Session

@dataclass
class UpdateWorkerFlowStatusRequest:
    position: PositionType
    times_executed: int


class WorkerFlowStatusService:

    def __init__(self, repo: WorkerFlowStatusRepository):
        self.repo = repo
    
    def update_worker_flow_status(self, session: Session, request: UpdateWorkerFlowStatusRequest) -> WorkerFlowStatus:
        instance = self.repo.find_first(session)
        if not instance:
            obj = WorkerFlowStatus.create(
                times_executed=request.times_executed,
                position=request.position
            ) 
            self.repo.add(instance=obj, session=session)
            return obj
        else:
            instance.update(
                times_executed=request.times_executed,
                position=request.position
            )

        return instance
    
    def delete_worker_flow_status(self, session: Session):
        instance = self.repo.find_first(session)
        self.repo.delete(session, instance)

    