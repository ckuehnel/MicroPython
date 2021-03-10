# Pi_Pico_Internals.py
# This sample program shows some information
# and uses some on-board resources to illustrate their query
# (c) 2021-03-09 Claus Kuehnel (info@ckuehnel.ch)

from machine import Timer
from machine import Pin
from machine import ADC

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

offset = ADC(0) # use grounded channel 0 for measuring ADC offset
temp   = ADC(4) # use channel 4 for measuring temperature
conversion_factor = 3.3 / (65536)

reading = offset.read_u16() * conversion_factor
print('ADC(0) offset voltage is {:3.3f} mV'.format(reading * 1000))

reading = temp.read_u16() * conversion_factor
# The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
# Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
temperature = 27 - (reading - 0.706)/0.001721
print('Internal temperature is {:3.1f} °C'.format(temperature))
