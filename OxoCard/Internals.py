'''
File:  Internals.py
needs: machine, time, sys, uos, ubinascii, esp, esp32, oxocard
based on https://www.tigerjython4kids.ch/index.php?inhalt_links=robotik/navigation.inc.php&inhalt_mitte=robotik/iot/push.inc.php

This program will show some information and the usage of some on-board ressources of Oxocard
2021-04-04 Claus Kühnel info@ckuehnel.ch
'''
import machine, time, sys, uos, ubinascii, esp, esp32
from machine import Timer
from oxocard import *

i = 0

def blink():
    global i
    i += 1
    if (i % 2):
        dot(3,3, BLUE)
    else:
        dot(3,3 ,BLACK)
    time.sleep_ms(100)
    

tim = Timer(0)
tim.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:blink())

  
print('\nThis program will show some information')
print('and the usage of some on-board ressources of Oxocard\n')

print('This is a {}'.format(uos.uname().machine))
print('Installed firmware version is {}\n'.format(uos.uname().version))
print('Platform is {}'.format(sys.platform))
print('Micropython version is {}'.format(sys.version))
print('Flash size is {:4.2f} MByte'.format(esp.flash_size()/1000000))
print('CPU frequency is {:3.0f} MHz'.format(machine.freq()/1000000))
print('Chip temperature is {:3.1f} *C'.format((esp32.raw_temperature()-32)*5/9))
print('Hall sensor readout is {}'.format(esp32.hall_sensor()))
print('One Neopixel of matrix display blinks w/ 1 Hz\n')

UID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
print('Length of UID is {} bytes'.format(int(len(UID)/2)))
print('UID is {}\n'.format(UID))
