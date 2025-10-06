from datetime import datetime
from zoneinfo import ZoneInfo
import requests

from configuration.application.use_case import ConfigurationQueryUseCase, GetConfigurationRequest

from shared_kernel.infra import logger
from worker.application.use_cases.step_definition_use_case import StepDefinitionQueryUseCase

class WorkerDeviceApiService:

    def __init__(
            self, config_query: ConfigurationQueryUseCase,
            step_definition_query: StepDefinitionQueryUseCase
    ) -> None:
        self.base_url = config_query.get_configuration(
            GetConfigurationRequest(
                name = "DEVICE_IP"
            )
        )[0].value
        self.step_definition_query = step_definition_query

    def start_offline_mode(self) -> None:
        full_path = f"{self.base_url}/startOfflineMode"
        logger.logger.info(f'Making request to: {full_path}')
        response = requests.post(full_path, json=self.__map_step_definition_body(), headers=self._get_headers())
        logger.logger.info(f'Response: {response.status_code}')

    def send_offline_data(self) -> None:
        full_path = f"{self.base_url}/sendOfflineData"
        logger.logger.info(f'Making request to: {full_path}')
        response = requests.post(full_path, headers=self._get_headers())
        logger.logger.info(f'Response: {response.status_code}')

    def __map_step_definition_body(self) -> dict[str, any]:
        step_definitions = self.step_definition_query.get_all_step_definition()
        map_result = map(lambda s: {
            "position": s.position,
            "sensor": s.sensor_type,
            "period": s.period,
            "delay": s.lead,
            "times_to_be_executed": s.get_times_to_be_executed()
        }, step_definitions)

        return {
            "step_defintions": list(map_result)
        }
    
    def _get_headers() -> dict[str, str]:
        now_bogota = datetime.now(ZoneInfo("America/Bogota"))
        date_str = now_bogota.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "-05:00"
        return {
            "Date": date_str
        }
