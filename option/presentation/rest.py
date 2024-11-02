from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from shared_kernel.infra.container import AppContainer

from option.application.use_case import OptionsQueryUseCase
from option.presentation.response import OptionResponse, OptionSchema
from option.domain.model.aggregate import Option


router = APIRouter(
    prefix="/option", tags=['option']
)

@router.get("/")
@inject
def get_alarms_definition(
    query: OptionsQueryUseCase = Depends(Provide[AppContainer.option.query]),
) -> OptionResponse:
    opts: List[Option] = query.get_options()
    return OptionResponse(
        detail="ok",
        result=[OptionSchema.from_orm(ad) for ad in opts]
    )
