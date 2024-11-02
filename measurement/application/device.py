from measurement.infra.api.device_repository import DeviceMeasureRepository

class MyService:
    def __init__(self, repository: DeviceMeasureRepository):
        self.repository = repository

    def get_entity_details(self, id: int):
        entity = self.repository.get(id)
        return entity