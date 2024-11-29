from __future__ import annotations
from typing import List
from shared_kernel.domain.value_object import ValueObject
import enum


class Unit(ValueObject, str, enum.Enum):
    CENTIGRADES = "°C"
    PERCENTAGE = "%"
    
    AMPERES = "A"
    MILI_AMPERE = "mA"  # Mili-amperios
    CENTI_AMPERE = "cA"  # Centi-amperios
    KILO_AMPERE = "kA"  # Kilo-amperios
    MEGA_AMPERE = "MA"  # Mega-amperios

    HERTZ = "Hz"
    KILO_HERTZ = "kHz"  # Kilohertz
    MEGA_HERTZ = "MHz"  # Megahertz

    MICRO_OHM = "μΩ"  # Micro-ohm
    OMHN = "Ω"  # Ohm
    KILO_OHM = "kΩ"  # Kilo-ohm
    MEGA_OHM = "MΩ"  # Mega-ohm
    MILI_OHM = "mΩ"  # Mili-ohm

    MICRO_VOLT = "μV"  # Micro-volt
    VOLTS = "V"
    MILI_VOLT = "mV"  # Mili-volt
    KILO_VOLT = "kV"  # Kilo-volt
    MEGA_VOLT = "MV"  # Mega-volt

    METERS_PER_SECOND_SQUARED = "m/s²"  # Aceleración (Vibración)
    MILLIMETERS_PER_SECOND = "mm/s"  # Velocidad (Vibración)
    MICRO_METERS_PER_SECOND_SQUARED = "μm/s²"  # Micro-aceleración (Vibración)

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
    FREQUENCY = "FREQUENCY"
    VOLTAGE = "VOLTAGE"

    @classmethod
    def get_units(cls, measure_type: str) -> List[Unit]:
        if measure_type == cls.ISOLATION:
            return [Unit.OMHN, Unit.MEGA_OHM, Unit.MICRO_OHM]
        elif measure_type == cls.RESISTANCE:
            return [Unit.OMHN, Unit.KILO_OHM, Unit.MEGA_OHM, Unit.MILI_OHM, Unit.MICRO_OHM]
        elif measure_type == cls.TEMPERATURE:
            return [Unit.CENTIGRADES]
        elif measure_type == cls.PRESSURE:
            return [Unit.PSI, Unit.BAR, Unit.PASCAL]
        elif measure_type == cls.VIBRATION:
            return [Unit.METERS_PER_SECOND_SQUARED, Unit.MILLIMETERS_PER_SECOND, Unit.MICRO_METERS_PER_SECOND_SQUARED]
        elif measure_type == cls.BATTERY:
            return [Unit.PERCENTAGE]
        elif measure_type == cls.FREQUENCY:
            return [Unit.HERTZ, Unit.KILO_HERTZ, Unit.MEGA_HERTZ]
        elif measure_type == cls.VOLTAGE:
            return [Unit.VOLTS, Unit.MILI_VOLT, Unit.KILO_VOLT, Unit.MEGA_VOLT, Unit.MICRO_VOLT]
        return []


class SensorType(ValueObject, str, enum.Enum):
    ISO = "ISO"
    RES = "RES"
    WELL = "WELL"

    @classmethod
    def get_measure_types(cls, sensor_type: str) -> List[MeasureType]:
        if sensor_type == cls.ISO:
            return [MeasureType.ISOLATION]
        elif sensor_type == cls.RES:
            return [MeasureType.RESISTANCE]
        elif sensor_type == cls.WELL:
            return [MeasureType.RESISTANCE, MeasureType.VIBRATION, MeasureType.TEMPERATURE]
        return []
