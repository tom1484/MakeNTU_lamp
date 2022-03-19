import time
import RPi.GPIO as gpio

class LED_IO:
    base_width = 32
    period = 0.01

    def __init__(self, pin):
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.OUT)
        self.pin = pin

    def output(self, data):
        start_stamp = time.time()
        index = 0
        for i in data:
            modifier = 2147483648
            if i < 0:
                i += modifier
            for j in range(self.base_width):
                curr_stamp = time.time()
                while curr_stamp - start_stamp <= index * self.period:
                    curr_stamp = time.time()

                print("check time complet!", curr_stamp)
                
                if i // modifier == 1 :
                    gpio.output(self.pin, gpio.HIGH)
                    print(1, end="")
                else:
                    gpio.output(self.pin, gpio.LOW)
                    print(0, end="")
                index = index + 1
                i = i % modifier
                modifier = modifier // 2
            print("")
        while time.time() - start_stamp <= index * self.period:
            pass
