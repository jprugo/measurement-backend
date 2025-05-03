import asyncio
from typing import List
from measurement.domain.model.value_object import SensorType
from worker.application.use_cases.worker_flow_status_use_case import UpdateWorkerFlowStatusRequest, WorkerFlowStatusUpdateCommand, WorkerFlowStatusQueryUseCase
from worker.domain.model.aggregate import StepDefinition, WorkerFlowStatus
from worker.domain.model.services.worker_service import WorkerService
from shared_kernel.infra import logger
from worker.domain.model.value_object import PositionType


class WorkerFlowService():
    def __init__(
                self, 
                worker_service: WorkerService,
                worker_flow_status_query: WorkerFlowStatusQueryUseCase,
                worker_flow_status_command: WorkerFlowStatusUpdateCommand
            ):
        self.worker_service = worker_service
        self.worker_flow_status_query = worker_flow_status_query
        self.worker_flow_status_command = worker_flow_status_command
        
    async def handle(self):
        
        status: WorkerFlowStatus = self.worker_flow_status_query.get_worker_flow_status()

        position = PositionType.from_value(status.position)
        logger.logger.info(f"Handling position: {position}")
        
        self.__try_send_stop_signal()

        # Step Definition Query
        data = self.worker_service.get_step_definition_from_position(position)
        if data:
            step = data[0]
            measure_history: List[float] = []
            
            times_to_be_executed = step.get_times_to_be_executed()
            times_executed = status.times_executed
            logger.logger.info(f'Times executed = {times_executed}')
            logger.logger.info(f'Times to be executed = {times_to_be_executed}')

            while times_executed < times_to_be_executed:
                try:
                    measures = self.worker_service.get_measure(step)

                    logger.logger.info('Saving measure and verifying alarm level')
                    for measure in measures:
                        self.worker_service.register_measure(measure, measure_history)
                        self.worker_service.verify_alarm_level(measure, measure_history)

                    logger.logger.info('End measure and verifying alarm level')

                    await self._lead_period(step)

                    self._prepare_next_iteration(position, times_executed)
                    times_executed += 1
                except:
                    logger.logger.error(
                        "!!!!!!!!!!!!!!! Can't reach device to get measures for position: [%s]!!!!!!!!!!!!!!!", 
                        position
                    )
                    raise Exception("Communication lost with the device.")

            await self._lead_final(step)
        else:
            position = PositionType.FIRST
        self._prepare_next_step(position, times_executed)

    def __try_send_stop_signal(self):
        try:
            logger.logger.info("*************** Sending stop signal ****************")
            self.worker_service.stop_measure()
        except Exception:
            self.worker_service._register_event(
                "ATENCION",
                "Error de comunicacion durante la orden de detención de sensor",
                None,
                None
            )
            logger.logger.info("!!!!!!!!!!!!!!! Can't send stop singal !!!!!!!!!!!!!!!")

    def _prepare_next_iteration(self, position: PositionType, times_executed: int):
        logger.logger.info("Moving to next iteration")
        times_executed += 1
        self._register_status(position, times_executed)

    def _prepare_next_step(self, position: PositionType, times_executed: int):
        next_position = self.worker_service.get_next_position(position)
        logger.logger.info(f"Moving to next step with position: {next_position}")
        
        times_executed = 1
        self._register_status(next_position, times_executed)

    def _register_status(self, position, times_executed: int):
        logger.logger.info(f"Saving status in DB: {position}")
        self.worker_flow_status_command.execute(
            UpdateWorkerFlowStatusRequest(
                position=position,
                times_executed=times_executed
            )
        )

    async def _lead_period(self, step: StepDefinition):
        logger.logger.info(f'Awaiting {step.period} seconds defined in period')
        await asyncio.sleep(step.period)
        logger.logger.info(f'Completed {step.period} seconds defined in period')

    async def _lead_final(self, step: StepDefinition):
        lead_time = step.lead * 60
        logger.logger.info(f'Waiting for lead time: {lead_time} seconds')
        await asyncio.sleep(lead_time)
        logger.logger.info(f'Completed for lead time: {lead_time} seconds')
