import logging
import time
from enum import Enum
from helper import is_crc_valid

I2C_ADDRESS = 0x58

class Command(Enum):
    Init_air_quality = (0x20, 0x03)
    Measure_air_quality = (0x20, 0x08)

class SGP30:
    def __init__(self, bus):
        self.bus = bus
        self._write_command(Command.Init_air_quality)

    def _write_command(self, command: Command):
        self.bus.write_i2c_block_data(I2C_ADDRESS, command.value[0], [command.value[1]])

    def read_data(self):
        """Wysyła żądanie pomiaru i zwraca wartości eCO2 oraz TVOC."""
        # Wyślij komendę: 'Measure_air_quality' (0x20, 0x08)
        self._write_command(Command.Measure_air_quality)

        # Odczekaj wymagany czas na przetworzenie pomiaru przez czujnik (ok. 12 ms)
        time.sleep(0.12)

        # Odczytaj 6 bajtów:
        # [eCO2 MSB, eCO2 LSB, eCO2 CRC, TVOC MSB, TVOC LSB, TVOC CRC]
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x00, 6)

        tvoc, eco2 = (0, 0)
        # Konwersja eCO2 (bajt 0 i 1)
        if not is_crc_valid(data[0:3]):
            eco2 = data[0] * 256 + data[1]
        else:
            logging.warning("CRC error")

        # Konwersja TVOC (bajt 3 i 4)
        if is_crc_valid(data[3:6]):
            tvoc = data[3] * 256 + data[4]
        else:
            logging.warning("CRC error")

        return eco2, tvoc