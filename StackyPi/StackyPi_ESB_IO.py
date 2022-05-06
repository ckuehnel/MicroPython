# StackyPi_ESB_IO.py
# 
# All StackyPi_ESB_xxx.py programs are used to test single fuctions
# of the Coral Environmental Sensor Board, a Raspberry Pi HAT.
# 
# On-board LED ist connected to GPIO15.
# Button is connected to GPIO27

# (c) 2022-05-05 Claus Kuehnel (info@ckuehnel.ch)
	
import machine, time, sys, uos

from machine import Timer, Pin, ADC

led = Pin(15, Pin.OUT)   # on-board LED of ESB
button = Pin(27, Pin.IN, Pin.PULL_UP)

t   = Timer()

def blink(Timer):
	led(1)
	time.sleep_ms(20)      # LED on for 20 milliseconds
	led(0)

t.init(period=1000, mode=Timer.PERIODIC, callback = blink)

print('\nThis program test basic functions of ESB connected to the StackyPi board')
print('The on-board LED of ESB blinks ones per second')
print('Press the on-board button for digital input')

for x in range(0, 10):
    print(button.value())   # get value, 0 or 1
    time.sleep(1)           # sleep for 1 second

print('Restart to repeat')
        