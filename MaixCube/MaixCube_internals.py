# MAiX_BiT_Internals.py
# This sample program shows some information
# and uses some on-board resources to illustrate their query
# (c) 2019-01-29 Claus Kuehnel (info@ckuehnel.ch

import machine, time, sys, uos
from Maix import freq

from machine import Timer
#from machine import Pin

'''
led = Pin(2, Pin.OUT)   # external LED on ESP32 DevKit

def blink():
    led.on()
    time.sleep_ms(20)      # LED on for 20 milliseconds
    led.off()
'''

print('\nThis program will show some information')
print('and the usage of some on-board ressources of MAiX_BiT Board\n')
#print('The external led blinks ones per second\n')
print('This is a {}'.format(uos.uname().machine))
print('Installed firmware version is {}\n'.format(uos.uname().version))
print('Platform is {}'.format(sys.platform))
print('Micropython version is {}'.format(sys.version))

#cpu_freq,kpu_freq = cpufreq.get_current_frequencies()
cpu_freq = freq.get_cpu()
kpu_freq = freq.get_kpu()
print('\nCPU frequency is {:3.0f} MHz'.format(cpu_freq))
print('KPU frequency is {:3.0f} MHz'.format(kpu_freq))

'''
print('Flash size is {:4.2f} MByte'.format(esp.flash_size()/1000000))

print('Chip temperature is {:3.1f} *C'.format((esp32.raw_temperature()-32)*5/9))
print('Hall sensor readout is {}\n'.format(esp32.hall_sensor()))

UID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
print('Length of UID is {} bytes'.format(int(len(UID)/2)))
print('UID is {}\n'.format(UID))

t = Timer(-1) # virtual (RTOS-based) timer
t.init(period=1000, mode=Timer.PERIODIC, callback=lambda f: blink())

print('Press the USR button to change the blink frequency')
print('Ctrl-C stopps the running program')

usrButton = Pin(0, Pin.IN, Pin.PULL_UP) 	# USR Button

global state
state = 0

while True:
    btn = usrButton.value()

    if btn == 1 and state == 0:
        state = 1
        #print('Button released')
        t.init(period=1000, mode=Timer.PERIODIC, callback=lambda f: blink())


    if btn == 0 and state ==1:
        state = 0
        #print('Button pressed')
        t.init(period=100, mode=Timer.PERIODIC, callback=lambda f: blink())











'''
