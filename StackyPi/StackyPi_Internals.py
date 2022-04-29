# StackyPi_Internals.py
# 
# This sample program shows some information 
# and uses some on-board resources to illustrate their query
# (c) 2021-02-04 Claus Kuehnel (info@ckuehnel.ch)
	
import machine, time, sys, uos

from machine import Timer, Pin, ADC

led = Pin(25, Pin.OUT)   # external LED on Pi Pico
t   = Timer()

temp   = ADC(4) # use channel 4 for measuring temperature
conversion_factor = 3.3 / (65536)

def blink(Timer):
	led(1)
	time.sleep_ms(20)      # LED on for 20 milliseconds
	led(0)

t.init(period=1000, mode=Timer.PERIODIC, callback = blink)

print('\nThis program will show some information about the StackyPi board')
print('and the usage of some on-board ressources of Raspberry Pi Pico Board\n')
print('The external led blinks ones per second\n')
print('This is a {}'.format(uos.uname().machine))
print('Installed firmware version is {}\n'.format(uos.uname().version))
print('Platform is {}'.format(sys.platform))
print('Micropython version is {}'.format(sys.version))
print('CPU frequency is {:3.0f} MHz'.format(machine.freq()/1e6))

# read value, 0-65535 across voltage range 0.0v - 3.3v
reading = temp.read_u16() * conversion_factor
    
# The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
# Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
intTemp = 27 - (reading - 0.706)/0.001721
print('On-Chip temperature is {:3.1f} °C'.format(intTemp))
        
        