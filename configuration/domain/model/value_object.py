import enum
from shared_kernel.domain.value_object import ValueObject

class TreatmentAs(ValueObject, str, enum.Enum):
    STRING = "STRING"
    FLOAT = "FLOAT"
    INT = "INT"