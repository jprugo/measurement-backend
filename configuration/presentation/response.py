from typing import List

from pydantic import BaseModel

from configuration.domain.model.value_object import TreatmentAs
from shared_kernel.presentation.response import BaseResponse


class ConfigurationSchema(BaseModel):
    id: int
    name: str
    value: str
    treatment_as: TreatmentAs

    class Config:
        orm_mode = True
        from_attributes=True


class ConfigurationResponse(BaseResponse):
    result: List[ConfigurationSchema]


class SetUpResponse(BaseModel):
    voltage: int    
