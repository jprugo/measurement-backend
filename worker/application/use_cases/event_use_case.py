from typing import Callable, ContextManager, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from alarming.domain.model.value_object import AlarmType
from measurement.domain.model.value_object import MeasureType
from worker.domain.model.aggregate import Event

from worker.infra.repository import EventRepository


class EventQueryUseCase:
    def __init__(self, repo: EventRepository, db_session: Callable[[], ContextManager[Session]]):
        self.repo = repo
        self.db_session = db_session

    def get(self) -> Event:
        with self.db_session() as session:
            value = self.repo.get_first(session)
            return value


class CreateEventCommandRequest(BaseModel):
    title: str
    description: str
    measure_type: Optional[MeasureType] = None
    alarm_type: Optional[AlarmType] = None


class DeleteEventCommand:
    def __init__(self, repo: EventRepository, db_session: Callable[[], ContextManager[Session]]):
        self.repo = repo
        self.db_session = db_session

    def execute(self) -> Event:
        with self.db_session() as session:
            event_saved = self.repo.get_first(session=session)
            self.repo.delete(session, event_saved)
            session.commit()


class CreateEventCommand:
    def __init__(self, repo: EventRepository, db_session: Callable[[], ContextManager[Session]]):
        self.repo = repo
        self.db_session = db_session

    def execute(self, request: CreateEventCommandRequest) -> Event:
        with self.db_session() as session:
            event_saved = self.repo.get_first(session=session)
            if event_saved is None:
                self.repo.add(
                    session=session,
                    instance=Event.create(
                        title=request.title,
                        description=request.description,
                        measure_type=request.measure_type.value if request.measure_type is not None else None,
                        alarm_type=request.alarm_type.value if request.alarm_type is not None else None
                    )
                )
                session.commit()
