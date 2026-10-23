import time

from test44 import read_sht31
from test58 import init_sgp30, read_sgp30
from mqtt import MQTTClient

if __name__ == "__main__":
    print("Łączenie do broakera mqtt")
    client = MQTTClient()

    print("Inicjalizacja czujnika SGP30...")
    init_sgp30()

    # Pierwsze kilka odczytów po resecie zawsze zwróci 400 ppm i 0 ppb,
    # ponieważ czujnik potrzebuje ok. 15 sekund na rozgrzanie baselinu.
    print("Rozpoczynanie pomiarów (czujnik stabilizuje się przez pierwsze 15s)...")

    while True:
        eco2, tvoc = read_sgp30()
        print(f"eCO2: {eco2} ppm | TVOC: {tvoc} ppb")

        celsius, humidity = read_sht31()
        print(f"temp: {celsius} C | humidity: {humidity} %")

        client.publish("sgp30",f"eCO2: {eco2} ppm | TVOC: {tvoc} ppb")
        client.publish("sht31",f"temp: {celsius} C | humidity: {humidity} %")

        # WAŻNE: Specyfikacja Sensirion wymaga wywoływania pomiaru
        # dokładnie co 1 sekundę, aby wewnętrzny algorytm kalibracji działał poprawnie.
        time.sleep(1.0)