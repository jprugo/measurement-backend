from sqlalchemy.orm import Query, Session
from typing import List

from alarming.domain.model.aggregate import AlarmDefinition, Alarm
from measurement.domain.model.value_object import MeasureType
from shared_kernel.infra.database.repository import  RDBRepository

class AlarmRepository(RDBRepository):
   
    @staticmethod
    def add(session: Session, instance: Alarm):
        session.add(instance)
        return instance
    
    
    @staticmethod
    def commit(session: Session):
        session.commit()


    @staticmethod
    def delete(session: Session, instance: Alarm):
        session.delete(instance)


    @staticmethod
    def get_by_id(session: Session, entity_id: int):
        return session.query(Alarm).get(entity_id)
    

    @staticmethod
    def get_all(session: Session) -> Query:
        return session.query(Alarm)


    @staticmethod
    def get_by_id(session: Session, entity_id: int):
        return session.query(Alarm).get(entity_id)


class AlarmDefinitionRepository(RDBRepository):

    @staticmethod
    def find_by_measure_type(session: Session, measure_type: MeasureType) -> Query:
        return session.query(AlarmDefinition).filter_by(measure_type=measure_type)


    @staticmethod
    def add(session: Session, instance: AlarmDefinition):
        existing_instance = session.query(AlarmDefinition).filter_by(id=instance.id).first()
    
        if existing_instance:
            return existing_instance
        else:
            session.add(instance)
            return instance
    

    @staticmethod
    def commit(session: Session):
        session.commit()


    @staticmethod
    def delete(session: Session, instance: AlarmDefinition):
        session.delete(instance)


    @staticmethod
    def get_by_id(session: Session, entity_id: int):
        return session.query(AlarmDefinition).get(entity_id)
    

    @staticmethod
    def get_all(session: Session,) -> Query:
        return session.query(AlarmDefinition)


    @staticmethod
    def get_by_id(session: Session, entity_id: int):
        return session.query(AlarmDefinition).get(entity_id)