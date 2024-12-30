from queue import Queue
from shared_kernel.infra.database.repository import RDBRepository

from sqlalchemy.orm import Session

from worker.domain.model.aggregate import Event, StepDefinition, WorkerFlowStatus
from worker.domain.model.value_object import PositionType

class EventRepository:
    
    def __init__(self):
        self.queue = Queue(5)

    def get(self):
        return self.queue.get()
    
    def add(self, instance: Event):
        self.queue.put(instance)


class StepDefinitionRepository(RDBRepository):
    
    @staticmethod
    def find_by_position(session: Session, position: PositionType):
        return session.query(StepDefinition).filter_by(position=position)


    @staticmethod
    def add(session: Session, instance: StepDefinition):
        existing_instance = session.query(StepDefinition).filter_by(id=instance.id).first()
    
        if existing_instance:
            return existing_instance
        else:
            session.add(instance)
            return instance
    

    @staticmethod
    def commit(session: Session):
        session.commit()


    @staticmethod
    def delete(session: Session, instance: StepDefinition):
        session.delete(instance)


    @staticmethod
    def get_by_id(session: Session, entity_id: int):
        return session.query(StepDefinition).get(entity_id)
    

    @staticmethod
    def get_all(session: Session):
        return session.query(StepDefinition).all()


    @staticmethod
    def get_by_id(session: Session, entity_id: int):
        return session.query(StepDefinition).get(entity_id)
    

class WorkerFlowStatusRepository(RDBRepository):
    
    @staticmethod
    def find_first(session: Session):
        return session.query(WorkerFlowStatus).first()


    @staticmethod
    def add(session: Session, instance: WorkerFlowStatus):
        session.add(instance)
        return instance
    
    @staticmethod
    def delete(session: Session, instance: WorkerFlowStatus):
        session.delete(instance)
