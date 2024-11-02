from dependency_injector import containers, providers

from alarming.infra.container import AlarmContainer
from configuration.infra.container import ConfigurationContainer
from measurement.infra.container import MeasurementContainer
from worker.infra.container import StepDefinitionContainer
from option.infra.container import OptionContainer


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "alarming.presentation.rest",
            "configuration.presentation.rest",
            "measurement.presentation.rest",
            "worker.presentation.rest",
            "option.presentation.rest"
        ]
    )

    alarm = providers.Container(AlarmContainer)
    configuration = providers.Container(ConfigurationContainer)
    measurement = providers.Container(MeasurementContainer)
    step_definition = providers.Container(StepDefinitionContainer)
    option = providers.Container(OptionContainer)