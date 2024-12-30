from typing import List
from measurement.application.use_cases.measurement_use_cases import (
    MeasurementQueryUseCase, 
    GetMeasurementRequest, 
    CreateMeasurementCommand, 
    CreateMeasurementRequest
)
from measurement.presentation.graphql.schema import MeasurementInput, MeasurementType


class BaseMutation:
    def __init__(self, measurement_command: CreateMeasurementCommand, measurement_query: MeasurementQueryUseCase):
        self.measurement_command = measurement_command
        self.measurement_query = measurement_query

    def _add_item(self, data: MeasurementInput):
        register_request = CreateMeasurementRequest(
            value=data.value,
            measure_type=data.sensor_type
        )
        return self.measurement_command.execute(register_request)

    def _get_all_items(self, request) -> List[MeasurementType]:
        return self.measurement_query.get_measures(
            GetMeasurementRequest(
                measure_type= request.sensor_type,
                start_date=request.start_date,
                end_date=request.end_date
            )
        )


class CreateMutation(BaseMutation):
    def __init__(self, measurement_command: CreateMeasurementCommand, measurement_query: MeasurementQueryUseCase):
        super().__init__(measurement_command, measurement_query)

    def add_measurement(self, data: MeasurementInput):
        self._add_item(data)


class Queries(BaseMutation):
    def __init__(self, measurement_command: CreateMeasurementCommand, measurement_query: MeasurementQueryUseCase):
        super().__init__(measurement_command, measurement_query)

    def get_all_measurements(self) -> List[MeasurementType]:
        return self._get_all_items()
