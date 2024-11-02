import requests

from configuration.application.use_case import ConfigurationQueryUseCase, GetConfigurationRequest
from measurement.domain.model.value_object import SensorType, MeasureDeviceResponse
from shared_kernel.infra import logger

class DeviceApiService:

    def __init__(self, config_query: ConfigurationQueryUseCase) -> None:
        self.base_url = config_query.get_configuration(
            GetConfigurationRequest(
                name = "DEVICE_IP"
            )
        )[0].value


    def fetch_data(self, sensor_type: SensorType) -> MeasureDeviceResponse:
        try:
            full_path = f"{self.base_url}/{sensor_type}"
            logger.logger.info(f'Making request to: {full_path}')
            response = requests.get(full_path, timeout=60)
            logger.logger.info(f'Response: {response.status_code}')
            return MeasureDeviceResponse(**response.json())
        except Exception as e:
            logger.logger.exception(e)
            return MeasureDeviceResponse(measures=[])


    def stop(self) -> None:
        full_path = f"{self.base_url}/stop"
        logger.logger.info(f'Making request to: {full_path}')
        response = requests.get(full_path)
        logger.logger.info(f'Response: {response.status_code}')
