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
    MILI_VOLTS = "mV"  # Mili-volts

    AMPER = "A"
    MILI_AMPER = "mA"  # Mili-ampers
    NANO_AMPER = "nA"  # Mili-ampers
    MICRO_AMPER = "uA"  # Mili-ampers

    MILLIMETERS_PER_SECOND = "mm/s"  # Velocidad (vibration)
    G_FORCES = "G"

    BAR = "bar"
    PASCAL = "Pa"  # Pascal
    PSI = "PSI"  # Pounds per square inch


class MeasureType(ValueObject, str, enum.Enum):
    ISOLATION = "ISOLATION"
    RESISTANCE = "RESISTANCE"
    TEMPERATURE = "TEMPERATURE"
    PRESSURE = "PRESSURE"
    VIBRATION = "VIBRATION"
    BATTERY = "BATTERY"

    # WELL
    TOOL_VOLTAGE = "TOOL_VOLTAGE"
    TOOL_CURRENT = "TOOL_CURRENT"

    # ISOLATION
    ISOLATION_VOLTAGE = "ISOLATION_VOLTAGE"
    LEAKEGE_CURRENT = "LEAKEGE_CURRENT"

    @classmethod
    def get_units(cls, measure_type: str) -> List[Unit]:
        if measure_type == cls.ISOLATION:
            return [Unit.MEGA_OHM, Unit.GIGA_OHM]
        elif measure_type == cls.RESISTANCE:
            return [Unit.OMHN, Unit.MILI_OHM,]
        elif measure_type == cls.TEMPERATURE:
            return [Unit.CENTIGRADES, Unit.FARENHEIT]
        elif measure_type == cls.PRESSURE:
            return [Unit.PSI, Unit.BAR, Unit.PASCAL]
        elif measure_type == cls.VIBRATION:
            return [Unit.MILLIMETERS_PER_SECOND, Unit.G_FORCES]
        elif measure_type == cls.BATTERY:
            return [Unit.PERCENTAGE]
        elif measure_type == cls.TOOL_VOLTAGE: # WELL
            return [Unit.VOLTS]
        elif measure_type == cls.TOOL_CURRENT: # WELL
            return [Unit.MICRO_AMPER, Unit.MILI_AMPER]
        elif measure_type == cls.ISOLATION_VOLTAGE: # ISO
            return [Unit.VOLTS]
        elif measure_type == cls.LEAKEGE_CURRENT: # ISO
            return [Unit.MICRO_AMPER, Unit.NANO_AMPER]
        return []


class SensorType(ValueObject, str, enum.Enum):
    ISO = "ISO"
    RES = "RES"
    WELL = "WELL"

    @classmethod
    def get_measure_types(cls, sensor_type: str) -> List[MeasureType]:
        if sensor_type == cls.ISO:
            return [
                MeasureType.ISOLATION,
                MeasureType.ISOLATION_VOLTAGE,
                MeasureType.LEAKEGE_CURRENT
            ]
        elif sensor_type == cls.RES:
            return [MeasureType.RESISTANCE]
        elif sensor_type == cls.WELL:
            return [
                MeasureType.PRESSURE,
                MeasureType.VIBRATION,
                MeasureType.TEMPERATURE,
                MeasureType.TOOL_CURRENT,
                MeasureType.TOOL_VOLTAGE
            ]
        return []
