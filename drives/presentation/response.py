from pydantic import BaseModel
from typing import List
from shared_kernel.presentation.response import BaseResponse

class DriveSchema(BaseModel):
    device: str
    mountpoint: str

    class Config:
        orm_mode = True
        from_attributes=True


class DriveResponse(BaseResponse):
    result: List[DriveSchema]