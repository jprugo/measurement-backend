import asyncio
from typing import List
from shared_kernel.infra.event_manager import EventManager
from worker.domain.model.worker_service import WorkerService, PositionType
from shared_kernel.infra import logger


class WorkerFlowService():
    def __init__(
                self, 
                worker_service: WorkerService,
                position: PositionType,
                times_executed: int
            ):
        self.worker_service = worker_service
        self.position = position
        self.times_executed = times_executed
        self.paused = False

    async def handle(self, event_manager: EventManager):
        logger.logger.info(f"Handling position: {self.position.value}")
        
        data = self.worker_service.get_step_definition_from_position(self.position)
        step = data[0]
        measure_history: List[float] = []
        self.times_to_be_executed = int(self._compute_iteration_time(step))
        
        logger.logger.info(f'Times to be executed = {self.times_to_be_executed}')
        
        while self.times_executed <= self.times_to_be_executed and self._has_to_run():
            logger.logger.info(f'{step.sensor_type} executed {self.times_executed} times')
            measures = self.worker_service.get_measure(step)
            logger.logger.info('Saving measure and verifying alarm level')

            for measure in measures:
                self.worker_service.register_measure(measure, measure_history)
                self.worker_service.verify_alarm_level(measure, measure_history)

            if self.times_executed != self.times_to_be_executed and self._has_to_run():
                await self._lead_period(step)

            self.times_executed += 1
        
        if self._has_to_run():
            await self._lead_final(step) 
        if not self.paused:
            self._prepare_next(event_manager)

    def _has_to_run(self):
        return not (self.paused)

    def _prepare_next(self, event_manager: EventManager):
        self.position = self.worker_service.get_next_position(self.position)
        self.times_executed = 1
        event_manager.publish(self.position.value, event_manager=event_manager)

    def _compute_iteration_time(self, step):
        return self._get_duration_in_secs(step) / step.period

    def _get_duration_in_secs(self, step):
        return step.duration * 60

    def _get_lead_in_secs(self, step):
        return step.lead * 60

    async def _lead_period(self, step):
        logger.logger.info(f'Awaiting {step.period} seconds defined in period')
        await asyncio.sleep(step.period)
        logger.logger.info(f'Completed {step.period} seconds defined in period')

    async def _lead_final(self, step):
        lead_time = step.lead * 60
        logger.logger.info(f'Waiting for lead time: {lead_time} seconds')
        await asyncio.sleep(lead_time)
        logger.logger.info(f'Completed for lead time: {lead_time} seconds')

    def handle_pause(self):
        logger.logger.info("Execution paused.")
        self.paused = True
    
    def handle_resume(self):
        logger.logger.info("Execution resumed.")
        self.paused = False