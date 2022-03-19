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
        high_signal_cnt = 0
        for i in data:
            modifier = 2147483648
            if i < 0:
                i += modifier * 2
            for j in range(self.base_width):
                curr_stamp = time.time()
                while curr_stamp - start_stamp <= index * self.period:
                    curr_stamp = time.time()

                
                if i // modifier == 1 :
                    gpio.output(self.pin, gpio.HIGH)
                    print(1, end="")
                    high_signal_cnt += 1
                else:
                    gpio.output(self.pin, gpio.LOW)
                    print(0, end="")
                index = index + 1
                i = i % modifier
                modifier = modifier // 2
            print("")

        perify = 2871633100 + high_signal_cnt % 2
        modifier = 2147483648
        for i in range(self.base_width):
            while time.time() - start_stamp <= index * self.period:
                pass
            if perify // modifier == 1:
                print(1, end="")
                gpio.output(self.pin, gpio.HIGH)
            else:
                print(0, end="")
                gpio.output(self.pin, gpio.LOW)
            index = index + 1
            perify = perify % modifier
            modifier = modifier // 2
        print("")
        while time.time() - start_stamp <= index * self.period:
            pass
