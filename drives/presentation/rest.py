import psutil

from typing import List
from fastapi import APIRouter
from shared_kernel.infra import logger

from drives.presentation.response import DriveResponse, DriveSchema


router = APIRouter(prefix="/drives", tags=['drives'])


@router.get("/")
def setup() -> DriveResponse:
    return DriveResponse(
        detail="ok",
        result= _get_usb_drives()
    )


def _get_usb_drives() -> List[DriveSchema]:
    try:
       result = psutil.disk_partitions()
       return list(map(lambda e: DriveSchema(
           device=e.device,
           mountpoint=e.mountpoint
       ), result))
    except Exception as e:
        logger.logger.exception(e)
        return []
