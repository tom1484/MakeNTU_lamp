import LiFi
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
test = LiFi.LED_IO(18)

test_data = [128, 128, 3, 2, 50, 50, -75, 100, 0, 0, -75, -75, 75, 75, 10, -75, -75, -75, 200, 20]

timer = 1
while timer:
    test.output(test_data);
    timer -= 1
