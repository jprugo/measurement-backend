import enum
from typing import List
from shared_kernel.domain.value_object import ValueObject
from measurement.domain.model.aggregate import Measure
import abc

class AlarmType(ValueObject, str, enum.Enum):
    DESVEST = "DESVEST"
    GREATER_THAN = "GREATER_THAN"
    LOWER_THAN = "LOWER_THAN"

class AlarmTypeBase(abc.ABC):
    @abc.abstractmethod
    def check(self, parametrized_value: float, measures: List[Measure]) -> bool:
        pass

class AlarmTypeFactory:
    @staticmethod
    def get_alarm(alarm_type: AlarmType):
        if alarm_type == AlarmType.DESVEST:
            return DesvestAlarmType()
        elif alarm_type == AlarmType.GREATER_THAN:
            return GreaterThanAlarmType()
        elif alarm_type == AlarmType.LOWER_THAN:
            return LowerThanAlarmType()
        raise ValueError("Invalid alarm type")
    

class LowerThanAlarmType(AlarmTypeBase):
    def check(self, parametrized_value: float, measures: List[Measure]) -> bool:
        return measures[-1] < parametrized_value


class GreaterThanAlarmType(AlarmTypeBase):
    def check(self, parametrized_value: float, measures: List[Measure]) -> bool:
        return measures[-1] > parametrized_value
    

class DesvestAlarmType(AlarmTypeBase):
    def check(self, parametrized_value: float, measures: List[Measure]) -> bool:
        last = measures[-1]
        return any(x for x in measures if abs(last - x) > parametrized_value)
