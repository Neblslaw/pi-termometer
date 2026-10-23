import logging
import time
from helper import is_crc_valid

I2C_ADDRESS = 0x44
class SHT31:

    def __init__(self, bus):
        self.bus = bus

    def read_data(self):
        # Send measurement command: high repeatability, no clock stretching (0x24, 0x00)
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x24, [0x00])
        time.sleep(0.15)

        # [temp MSB, temp LSB, temp CRC] [hum MSB, hum LSB, hum CRC]
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x00, 6)

        # Convert temperature
        if is_crc_valid(data[0:3]):
            temp_raw = data[0] * 256 + data[1]
            celsius = -45.0 + (175.0 * temp_raw / 65535.0)
        else:
            logging.warning("CRC error")

        # Convert humidity
        if is_crc_valid(data[3:6]):
            hum_raw = data[3] * 256 + data[4]
            humidity = 100.0 * hum_raw / 65535.0
        else:
            logging.warning("CRC error")


        return celsius, humidity


