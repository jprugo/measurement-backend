from __future__ import annotations
from shared_kernel.domain.entity import AggregateRoot
from dataclasses import dataclass
from configuration.domain.model.value_object import TreatmentAs

dataclass(eq=False)
class Configuration(AggregateRoot):
    id: int
    name: str
    value: str
    treatment_as: TreatmentAs
    
    @classmethod
    def create(
        cls, name: str, value: str, treatment_as: TreatmentAs
    ) -> Configuration:
        # Action
        return cls(
            name = name,
            value = value,
            treatment_as= treatment_as
        )

    def update(self, value: str):
        self.value = value
