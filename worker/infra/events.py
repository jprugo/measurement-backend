from worker.domain.model.aggregate import PositionType
from pydantic import BaseModel

class StepDefinitionCompleted(BaseModel):
    position: PositionType