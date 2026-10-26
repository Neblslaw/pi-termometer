import datetime
import time
from sched import scheduler

from gpiozero import LED
from SGP30 import SGP30
from SHT31 import SHT31
from Scheduler import Scheduler
from mqtt import MQTTClient
import json

import smbus2

# Pobranie szyny I2C (domyślna dla większości modeli Raspberry Pi)
bus = smbus2.SMBus(1)
green = LED(26)
red = LED(19)


def metoda():
    print(datetime.datetime.now())

    eco2, tvoc = sgp30.read_data()
    print(f"eCO2: {eco2} ppm | TVOC: {tvoc} ppb")

    celsius, humidity = sht31.read_data()
    print(f"temp: {celsius} C | humidity: {humidity} %")

    data = {
        "eCO2": eco2,
        "TVOC": tvoc,
        "temp": celsius,
        "humidity": humidity
    }

    client.publish("building/conference_room_1/air", json.dumps(data))

    if eco2 >= 1000:
        green.off()
        red.on()
    else:
        green.on()
        red.off()
    # WAŻNE: Specyfikacja Sensirion wymaga wywoływania pomiaru
    # dokładnie co 1 sekundę, aby wewnętrzny algorytm kalibracji działał poprawnie.
    # time.sleep(1.0)

if __name__ == "__main__":
    scheduler = Scheduler(1,metoda)

    green.on()
    red.on()
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

    scheduler.start()