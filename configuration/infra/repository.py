from sqlalchemy.orm import Query, Session
from configuration.domain.model.aggregate import Configuration
from shared_kernel.infra.database.repository import RDBRepository

class ConfigurationRepository(RDBRepository):
    
    @staticmethod
    def find_by_name(session: Session, name: str) -> Query:
        return session.query(Configuration).filter_by(name=name)
    

    @staticmethod
    def add(session: Session, instance: Configuration):
        existing_instance = session.query(Configuration).filter_by(id=instance.id).first()
    
        if existing_instance:
            return existing_instance
        else:
            session.add(instance)
            return instance


    @staticmethod
    def commit(session: Session):
        session.commit()


    @staticmethod
    def delete(session: Session, instance: Configuration):
        session.delete(instance)


    @staticmethod
    def get_by_id(session: Session, entity_id: int):
        return session.query(Configuration).get(entity_id)
    

    @staticmethod
    def get_all(session: Session) -> Query:
        return session.query(Configuration)


    @staticmethod
    def get_by_id(session: Session, entity_id: int):
        return session.query(Configuration).get(entity_id)

