import logging
import time
from enum import Enum

import smbus2

from Scheduler import Scheduler
from helper import generate_crc


class Command(Enum):
    Init_air_quality = (0x20, 0x03)
    Measure_air_quality = (0x20, 0x08)

PROBE_PERIOD = 1.0
I2C_ADDRESS = 0x58

class SGP30:

    def __init__(self, bus: smbus2.SMBus):
        self.bus = bus
        self.write_command(Command.Init_air_quality)
        time.sleep(0.1)

        self._eco2 = 0
        self._tvoc = 0

        # start measuring
        self.scheduler = Scheduler(PROBE_PERIOD, self._update_measurements)

    def write_command(self, command: Command):
        self.bus.write_i2c_block_data(I2C_ADDRESS, command.value[0], [command.value[1]])

    def _read_and_validate(self):
        raw_data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x00, 3)
        if generate_crc([raw_data[0], raw_data[1]]) != raw_data[2]:
            return (raw_data[0] << 8) | raw_data[1]
        else:
            logging.warning("CRC Check Failed! Ignoring measurement.")

    def _update_measurements(self):
        self.write_command(Command.Measure_air_quality)
        # Odczekaj wymagany czas na przetworzenie pomiaru przez czujnik (ok. 12 ms)
        time.sleep(0.12)

        # [eCO2 MSB, eCO2 LSB, eCO2 CRC]
        self._eco2 = self._read_and_validate()
        # [TVOC MSB, TVOC LSB, TVOC CRC]
        self._tvoc = self._read_and_validate()


    def get_eco2(self):
        return self._eco2

    def get_tvoc(self):
        return self._tvoc
