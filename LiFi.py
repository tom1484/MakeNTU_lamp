import time
import RPi.GPIO as gpio

class LED_IO:
    base_width = 32
    period = 0.00001

    def __init__(self, pin):
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.OUT)
        self.pin = pin

    def output(self, data):
        index = 0
        high_signal_cnt = 0
        ret_list = [];
        for i in data:
            modifier = 2147483648
            if i < 0:
                i += modifier * 2
            for j in range(self.base_width):
                ret_list.append(i // modifier);
                i = i % modifier
                modifier = modifier // 2

        perify = 2871633100 + high_signal_cnt % 2
        modifier = 2147483648
        for i in range(self.base_width):
            ret_list.append(perify // modifier);
            perify = perify % modifier
            modifier = modifier // 2

        start_stamp = time.time()
        print(start_stamp)
        for signal in ret_list:
            while time.time() - start_stamp <= index * self.period:
                pass
            if signal == 1:
                gpio.output(self.pin, gpio.HIGH)
            else:
                gpio.output(self.pin, gpio.LOW)
            print(signal, end="")
            index += 1;
