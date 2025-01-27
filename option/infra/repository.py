from option.domain.model.value_object import ApplicationType
from option.domain.model.aggregate import Option

from shared_kernel.infra import logger


class OptionRepository:
    def get_all(self, application_type : ApplicationType):
        if application_type == ApplicationType.FULL:
            return  [
                Option(title="Aislamiento", resource_path= "aislamiento.html"),
                Option(title="Resistencia", resource_path= "resistencia.html"),
                Option(title="Temperatura", resource_path= "temperatura.html"),
                Option(title="Vibracion", resource_path= "vibracion.html"),
                Option(title="Presión", resource_path= "presion.html"),
                Option(title="Voltaje", resource_path= "voltaje.html"),
                Option(title="Corriente", resource_path= "corriente.html"),
            ]
        elif application_type == ApplicationType.LIGHT:
            return [
                Option(title="Aislamiento", resource_path= "aislamiento.html"),
                Option(title="Resistencia", resource_path= "resistencia.html"),
            ]
        else:
            logger.logger.error('Not mapped')
            raise ValueError('Application type incorrect')