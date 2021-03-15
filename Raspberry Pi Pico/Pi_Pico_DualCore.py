# Pi_Pico_DualCore.py
# Demonstration of Dual Core Operation
# 2021-03-15 Claus Kühnel info@ckuehnel.ch

import time, _thread, machine

def task(n, delay):
    led = machine.Pin(25, machine.Pin.OUT)
    lock = _thread.allocate_lock()
    with lock:
        print('\nCore 1 started')
    for i in range(n):
        led.high()
        time.sleep(delay)
        led.low()
        time.sleep(delay)
    lock = _thread.allocate_lock()
    with lock:
        print('\nCore 1 finished')
    _thread.exit()

print('Core 0 running')

# start program task in Core 1
_thread.start_new_thread(task, (10, 0.5))

while True:
    lock = _thread.allocate_lock()
    with lock:
        print('.', end = '')
    time.sleep(.5)
    