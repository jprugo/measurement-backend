from worker.infra.api.device_api_service import WorkerDeviceApiService

class SendOfflineModeSignalCommand:
    def __init__(self, service: WorkerDeviceApiService):
        self.service = service

    def execute(self) -> None:
        self.service.start_offline_mode()

class SendOfflineDataSignalCommand:
    def __init__(self, service: WorkerDeviceApiService):
        self.service = service

    def execute(self) -> None:
        self.service.send_offline_data()