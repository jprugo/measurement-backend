from typing import  List

from measurement.infra.api.device_api_service import DeviceApiService
from measurement.infra.api.response import DeviceMeasure
from measurement.application.use_cases.measurement_use_cases import CreateMeasurementCommand, DeviceMeasurementQueryUseCase, CreateMeasurementRequest

from worker.application.use_cases.step_definition_use_case import CreateEventCommand, StepDefinitionQueryUseCase, CreateEventCommandRequest
from worker.domain.model.aggregate import StepDefinition
from worker.domain.model.value_object import PositionType

from alarming.application.use_cases.alarm_definition_use_cases import AlarmDefinitionQueryUseCase
from alarming.application.use_cases.alarm_use_cases import CreateAlarmCommand
from alarming.domain.model.aggregate import AlarmDefinition
from alarming.domain.model.value_object import AlarmTypeFactory
from alarming.domain.model.services import RegisterAlarmRequest

import pygame

from shared_kernel.infra import logger

class NotConfiguredPositionError(Exception):
    pass

class WorkerService:
    
    def __init__(
        self, 
        # WORKER
        step_definition_query: StepDefinitionQueryUseCase,
        # MEASUREMENT
        measurement_command: CreateMeasurementCommand,
        measurement_query: DeviceMeasurementQueryUseCase,
        device_api_service: DeviceApiService, 
        # ALARM
        alarm_def_query: AlarmDefinitionQueryUseCase,
        alarm_command: CreateAlarmCommand,
        event_command: CreateEventCommand
    ):
        self.step_definition_query = step_definition_query
        # MEASUREMENT
        self.measurement_command = measurement_command
        self.measurement_query = measurement_query

        # DEVICE
        self.device_api_service = device_api_service

        # ALARM
        self.alarm_query = alarm_def_query
        self.alarm_command = alarm_command
        # ALARM
        self.event_command = event_command

    def get_step_definition_from_position(self, position):
        data = self.step_definition_query.find_by_position(position=position)
        if not data:
            raise NotConfiguredPositionError('Data not found for the given position.')
        return data

    def get_measure(self, step: StepDefinition) -> List[DeviceMeasure]:
        logger.logger.info(f"Getting {step.sensor_type} measure from device")
        try:
            return self.measurement_query.get_measures(step.sensor_type)
        except Exception as e:
            self._register_event(
                "Alerta comunicacion",
                "Ocurrio un error de comunicacion con el dispositivo"
            )
            logger.logger.exception(e)

    def stop_measure(self) -> None:
        logger.logger.info(f"Sending stop message...")
        return self.device_api_service.stop()

    def register_measure(self, measure: DeviceMeasure, measure_history: List[float]):
        measure_history.append(measure.value)
        self.measurement_command.execute(
            CreateMeasurementRequest(
                value=measure.value,
                measure_type=measure.measure_type,
                detail= measure.detail
            )
        )

    def verify_alarm_level(self, measure: DeviceMeasure, measure_history: List[float]):
        alarm_definitions = self.alarm_query.get_alarms_definition_by_measure_type(measure_type=measure.measure_type)
        if alarm_definitions:
            alarm_definition = alarm_definitions[0]
            if alarm_definition.enabled:
                alarm_type = AlarmTypeFactory.get_alarm(alarm_type=alarm_definition.alarm_type)
                if alarm_type.check(parametrized_value=alarm_definition.config_value, measures=measure_history):
                    self._trigger_alarm(alarm_definition=alarm_definition, measure_value= measure.value)

    def get_next_position(self, current_enum: PositionType) -> PositionType:
        enum_members = list(PositionType)
        current_index = enum_members.index(current_enum)
        next_index = (current_index + 1) % len(enum_members)
        return enum_members[next_index]
    
    def _reproduce(self, sound_path: str):
        try:
            logger.logger.info(f'Playing {sound_path}')
            pygame.mixer.init()
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        except:
            logger.logger.error("Error while playing sound")            

    def _save_alarm(self, alarm_definition: AlarmDefinition, measure_value: float):
        self.alarm_command.execute(
            request=RegisterAlarmRequest(
                alarm_type= alarm_definition.alarm_type,
                value= measure_value,
                config_value= alarm_definition.config_value,
                measure_type= alarm_definition.measure_type
            )
        )

    def _trigger_alarm(self, alarm_definition: AlarmDefinition, measure_value: float):
        self._register_event(
            "Alerta medición",
            f"Alarma disparada {alarm_definition.alarm_type} durante la medicion de {alarm_definition.measure_type}"
        )
        self._reproduce(sound_path= alarm_definition.sound_path)
        self._save_alarm(alarm_definition=alarm_definition, measure_value=measure_value)

    def _register_event(self, title, description):
        self.event_command.execute(
            CreateEventCommandRequest(
                title=title,
                description=description
            )
        )
