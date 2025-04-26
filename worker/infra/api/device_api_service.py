import requests

from configuration.application.use_case import ConfigurationQueryUseCase, GetConfigurationRequest
from shared_kernel.infra import logger

class WorkerDeviceApiService:

    def __init__(self, config_query: ConfigurationQueryUseCase) -> None:
        self.base_url = config_query.get_configuration(
            GetConfigurationRequest(
                name = "DEVICE_IP"
            )
        )[0].value

    def start_offline_mode(self) -> None:
        full_path = f"{self.base_url}/startOfflineMode"
        logger.logger.info(f'Making request to: {full_path}')
        response = requests.get(full_path)
        logger.logger.info(f'Response: {response.status_code}')
