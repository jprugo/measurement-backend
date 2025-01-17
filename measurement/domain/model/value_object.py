from __future__ import annotations
from typing import List
from shared_kernel.domain.value_object import ValueObject
import enum


class Unit(ValueObject, str, enum.Enum):
    CENTIGRADES = "°C"
    FARENHEIT = "°F"
    PERCENTAGE = "%"

    # Resistance
    OMHN = "Ω"  # Ohm
    MILI_OHM = "mΩ"  # Mili-ohm

    # Isolation
    MEGA_OHM = "MΩ"  # Mega-ohm
    GIGA_OHM = "GΩ"  # Mega-ohm

    VOLTS = "V"
   
    MILLIMETERS_PER_SECOND = "mm/s"  # Velocidad (Vibración)
    G_FORCES = "g"

    BAR = "bar"
    PASCAL = "Pa"  # Pascal
    PSI = "PSI"  # Pounds per square inch


class MeasureType(ValueObject, str ,enum.Enum):
    ISOLATION = "ISOLATION"
    RESISTANCE = "RESISTANCE"
    TEMPERATURE = "TEMPERATURE"
    PRESSURE = "PRESSURE"
    VIBRATION = "VIBRATION"
    BATTERY = "BATTERY"
    VOLTAGE = "VOLTAGE"

    @classmethod
    def get_units(cls, measure_type: str) -> List[Unit]:
        if measure_type == cls.ISOLATION:
            return [Unit.MEGA_OHM, Unit.GIGA_OHM]
        elif measure_type == cls.RESISTANCE:
            return [Unit.OMHN, Unit.MEGA_OHM,]
        elif measure_type == cls.TEMPERATURE:
            return [Unit.CENTIGRADES, Unit.FARENHEIT]
        elif measure_type == cls.PRESSURE:
            return [Unit.PSI, Unit.BAR, Unit.PASCAL]
        elif measure_type == cls.VIBRATION:
            return [Unit.MILLIMETERS_PER_SECOND, Unit.G_FORCES]
        elif measure_type == cls.BATTERY:
            return [Unit.PERCENTAGE]
        elif measure_type == cls.VOLTAGE:
            return [Unit.VOLTS]
        return []


class SensorType(ValueObject, str, enum.Enum):
    ISO = "ISO"
    RES = "RES"
    WELL = "WELL"

    @classmethod
    def get_measure_types(cls, sensor_type: str) -> List[MeasureType]:
        if sensor_type == cls.ISO:
            return [MeasureType.ISOLATION, MeasureType.VOLTAGE]
        elif sensor_type == cls.RES:
            return [MeasureType.RESISTANCE]
        elif sensor_type == cls.WELL:
            return [MeasureType.PRESSURE, MeasureType.VIBRATION, MeasureType.TEMPERATURE]
        return []
