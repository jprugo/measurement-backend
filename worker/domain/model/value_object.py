from shared_kernel.domain.value_object import ValueObject
import enum

class PositionType(ValueObject, str, enum.Enum):
    FIRST = "FIRST"
    SECOND = "SECOND"
    THIRD = "THIRD"