
from typing import List
from measurement.domain.model.value_object import SensorType, DeviceMeasure
from measurement.infra.api.device_api_service import DeviceApiService
from shared_kernel.infra.database.repository import RDBRepository

class DeviceMeasureRepository(RDBRepository):

    @staticmethod
    def get(api_service: DeviceApiService, sensor_type: SensorType) -> List[DeviceMeasure]:
        return api_service.fetch_data(sensor_type=sensor_type).measures
