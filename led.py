from gpiozero import LED
from time import sleep

green = LED(26)
red = LED(19)

while True:
    green.on()
    red.off()
    sleep(1)
    green.off()
    red.on()
    sleep(1)
