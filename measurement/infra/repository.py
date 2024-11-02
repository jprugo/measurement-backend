from sqlalchemy.orm import Session, Query

from datetime import datetime
from measurement.domain.model.aggregate import Measure, MeasureType

from shared_kernel.infra.database.repository import RDBRepository

from sqlalchemy import func, and_
from sqlalchemy.orm import aliased

class MeasurementRepository(RDBRepository):

    @staticmethod
    def find_by_sensor_type_detail_and_date_range(session: Session, measure_type: MeasureType, start_date: datetime, end_date: datetime, detail) -> Query:
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        query = session.query(Measure).filter(
            Measure.measure_type == measure_type,
            Measure.created_at >= start_date,
            Measure.created_at <= end_date,
        )
        
        if detail and detail != "Todos":
            query = query.filter(Measure.detail == detail)

        return query.all()


    @staticmethod
    def find_latest_records_for_all_measure_types(session: Session):
        MeasureAlias = aliased(Measure)

        measure_types = session.query(Measure.measure_type).distinct().all()

        latest_records = []

        for measure_type in measure_types:
            measure_type_value = measure_type[0]

            details = session.query(Measure.detail).filter(
                Measure.measure_type == measure_type_value
            ).distinct().all()

            for detail in details:
                detail_value = detail[0]

                latest_record = session.query(Measure).filter(
                    and_(
                        Measure.measure_type == measure_type_value,
                        Measure.detail == detail_value,
                        Measure.created_at == session.query(
                            func.max(MeasureAlias.created_at)
                        ).filter(
                            and_(
                                MeasureAlias.measure_type == measure_type_value,
                                MeasureAlias.detail == detail_value
                            )
                        )
                    )
                ).one_or_none()

                if latest_record:
                    latest_records.append(latest_record)

        return latest_records
    
    @staticmethod
    def add(session: Session, instance: Measure):
        session.add(instance)
        return instance
    
    
    @staticmethod
    def commit(session: Session):
        session.commit()


    @staticmethod
    def delete(session: Session, instance: Measure):
        session.delete(instance)


    @staticmethod
    def get_by_id(session: Session, entity_class: type, entity_id: int):
        return session.query(entity_class).get(entity_id)
    

    @staticmethod
    def get_all(session: Session, entity_class: type):
        return session.query(entity_class).all()


    @staticmethod
    def get_by_id(session: Session, entity_class: type, entity_id: int):
        return session.query(entity_class).get(entity_id)
