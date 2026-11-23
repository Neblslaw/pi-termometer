import time

from gpiozero import LED
from SGP30 import SGP30
from SHT31 import SHT31
from epaper.examples.epd_3in0g_test import Screen
from mqtt import MQTTClient
import json

import smbus2

from waveshare_epd import epd3in0g

# Pobranie szyny I2C (domyślna dla większości modeli Raspberry Pi)
bus = smbus2.SMBus(1)
green = LED(26)
red = LED(19)

if __name__ == "__main__":
    try:
        screen = Screen()
        green.on()
        red.on()
        reading_count = 0
        print("Łączenie do broakera mqtt")
        client = MQTTClient()

        # Pobranie szyny I2C (domyślna dla większości modeli Raspberry Pi)
        bus = smbus2.SMBus(1)


        print("Inicjalizacja czujników...")
        sgp30 = SGP30(bus)
        sht31 = SHT31(bus)

        # Pierwsze kilka odczytów po resecie zawsze zwróci 400 ppm i 0 ppb,
        # ponieważ czujnik potrzebuje ok. 15 sekund na rozgrzanie baselinu.
        print("Rozpoczynanie pomiarów (czujnik stabilizuje się przez pierwsze 15s)...")
        time.sleep(15)

        red.off()

        while True:
            next_reading = time.time() + 1
            eco2, tvoc = sgp30.read_data()
            print(f"eCO2: {eco2} ppm | TVOC: {tvoc} ppb")

            celsius, humidity = sht31.read_data()
            print(f"temp: {celsius} C | humidity: {humidity} %")

            if reading_count % 15 == 0:
                data = {
                    "eCO2": eco2,
                    "TVOC": tvoc,
                    "temp": celsius,
                    "humidity": humidity
                }

                client.publish("team2/building/conference_room_1/air", json.dumps(data))

            if eco2 >= 1000:
                green.off()
                red.on()
            else:
                green.on()
                red.off()

            if reading_count % 3000:
                data = {
                    "eCO2": eco2,
                    "TVOC": tvoc,
                    "temp": celsius,
                    "humidity": humidity
                }
                screen.draw(data)

            reading_count = reading_count + 1

            # Calculate how much time is left until the next reading
            sleep_time = next_reading - time.time()

            # Sleep only if we haven't already passed the target time
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                print("timing warning: ", sleep_time)

    except KeyboardInterrupt:
        epd3in0g.epdconfig.module_exit(cleanup=True)
        exit()



