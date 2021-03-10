# Pi_Pico_Internals.py
# This sample program shows some information
# and uses some on-board resources to illustrate their query
# (c) 2021-03-09 Claus Kuehnel (info@ckuehnel.ch)

from machine import Timer
from machine import Pin

import sys, uos, ubinascii

def tick(timer):
    led.toggle()

led = Pin(25, Pin.OUT) # green LED on Pi Pico
timer = Timer()
timer.init(freq=2, mode=Timer.PERIODIC, callback=tick)

print('\nThis program will show some information')
print('and the usage of some on-board ressources of Raspberry Pi Pico Board\n')
print('The external led blinks ones per second\n')
print('This is a {}'.format(uos.uname().machine))
print('Installed firmware version is {}\n'.format(uos.uname().version))
print('Platform is {}'.format(sys.platform))
print('Micropython version is {}'.format(sys.version))
print('CPU frequency is {:3.0f} MHz'.format(machine.freq()/1e6))

UID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
print('Length of UID is {} bytes'.format(int(len(UID)/2)))
print('UUID is {}\n'.format(UID))
