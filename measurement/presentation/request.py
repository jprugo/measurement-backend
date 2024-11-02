from datetime import datetime
from pydantic import BaseModel

class ExportDTO(BaseModel):
    start_date: datetime
    end_date: datetime
    mountpoint: str