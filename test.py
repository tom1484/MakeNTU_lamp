import RPi.GPIO as gpio
from time import sleep

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)

while True:
    gpio.output(17, gpio.HIGH)
    sleep(1)
    gpio.output(17, gpio.LOW)
    sleep(1)
