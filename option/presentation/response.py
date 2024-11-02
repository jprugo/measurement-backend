from typing import List

from pydantic import BaseModel
from shared_kernel.presentation.response import BaseResponse


class OptionSchema(BaseModel):
    title: str
    resource_path: str

    class Config:
        orm_mode = True
        from_attributes=True


class OptionResponse(BaseResponse):
    result: List[OptionSchema]
