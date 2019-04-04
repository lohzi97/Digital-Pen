import time

def bluetoothScan(led_1, led_2, led_3, led_4):
    
    led_1.blink(on_time=0.25, off_time=1.5)
    time.sleep(0.25)
    led_2.blink(on_time=0.25, off_time=1.5)
    time.sleep(0.25)
    led_3.blink(on_time=0.25, off_time=1.5)
    time.sleep(0.25)
    led_4.blink(on_time=0.25, off_time=1.5)

def bluetoothConnected(led_1, led_2, led_3, led_4):

    led_1.on()
    led_2.on()
    led_3.on()
    led_4.on()
    time.sleep(3)
    led_1.off()
    led_2.off()
    led_3.off()
    led_4.off()

def bluetoothFailed(led_1, led_2, led_3, led_4):

    led_1.blink(on_time=0.5, off_time=0.5)
    led_2.blink(on_time=0.5, off_time=0.5)
    led_3.blink(on_time=0.5, off_time=0.5)
    led_4.blink(on_time=0.5, off_time=0.5)

def started(led_1, led_2, led_3, led_4):

    led_1.off()
    led_2.off()
    led_3.off()
    led_4.off()
