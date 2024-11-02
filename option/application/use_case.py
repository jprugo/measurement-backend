from typing import  List

from option.infra.repository import OptionRepository
from option.domain.model.aggregate import Option
from option.domain.model.value_object import ApplicationType


class OptionsQueryUseCase:
    def __init__(self, repo: OptionRepository):
        self.repo = repo

    def get_options(self) -> List[Option]:
        return self.repo.get_all(application_type = ApplicationType.FULL)
