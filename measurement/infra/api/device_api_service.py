from functools import wraps
import time
import requests

from configuration.application.use_case import ConfigurationQueryUseCase, GetConfigurationRequest
from measurement.domain.model.value_object import SensorType
from shared_kernel.infra import logger
from measurement.infra.api.response import MeasureDeviceResponse

def retry_request(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except (requests.RequestException, ValueError) as e:
                    attempt += 1
                    logger.logger.exception(f"Attempt {attempt} failed: {e}")
                    if attempt < max_retries:
                        time.sleep(delay)
                    else:
                        logger.logger.error(f"Max retries reached for {func.__name__}. Raising exception.")
                        raise Exception(f"Failed to fetch data after {max_retries} attempts.") from e
        return wrapper
    return decorator

class DeviceApiService:

    def __init__(self, config_query: ConfigurationQueryUseCase) -> None:
        self.base_url = config_query.get_configuration(
            GetConfigurationRequest(
                name = "DEVICE_IP"
            )
        )[0].value

    @retry_request(max_retries=3, delay=2)
    def fetch_data(self, sensor_type: SensorType) -> MeasureDeviceResponse:
        full_path = f"{self.base_url}/{sensor_type}"
        logger.logger.info(f'Making request to: {full_path}')
        response = requests.get(full_path, timeout=60)
        response.raise_for_status()
        logger.logger.info(f'Response: {response.status_code}')
        return MeasureDeviceResponse(**response.json())


    def stop(self) -> None:
        full_path = f"{self.base_url}/stop"
        logger.logger.info(f'Making request to: {full_path}')
        response = requests.get(full_path)
        logger.logger.info(f'Response: {response.status_code}')
