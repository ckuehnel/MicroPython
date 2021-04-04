'''
File:  battery.py
needs: machine, oxocard
based on https://www.tigerjython4kids.ch/index.php?inhalt_links=robotik/navigation.inc.php&inhalt_mitte=robotik/iot/push.inc.php

This program will show the battery voltage internally measured.
One Neopixel of the Matrix Display is used as an indicator for the battery level.
2021-04-04 Claus Kühnel info@ckuehnel.ch
'''

from oxocard import *
from machine import ADC, Pin

MAX_BATTERY_VOLTAGE = 4400 # 1.1V / 100kOhm * 400kOhm
LOW_BATTERY_VOLTAGE = 3250
MIN_BATTERY_VOLTAGE = 3005

adc = ADC(Pin(34))          # create ADC object on ADC pin
#print(adc.read())           # read value, 0-4095 across voltage range 0.0v - 1.0v = 1/4 Vbat

adc.atten(ADC.ATTN_6DB)     # set 6 dB input attenuation (voltage range roughly 0.0v - 2 v)
adc.width(ADC.WIDTH_12BIT)  # set 12 bit return values (returned range 0-4095)

count = adc.read()          # read value using the newly configured attenuation and width
print(count/512)

while True:
    Vbat = count*1000/512
    print ('Battery Voltage = {} mV'.format(int(round(Vbat,0))))

    if Vbat > LOW_BATTERY_VOLTAGE:
        dot(7, 7, GREEN)
    elif Vbat >= MIN_BATTERY_VOLTAGE and Vbat <= LOW_BATTERY_VOLTAGE:
        dot(7, 7, YELLOW)
    else:
        dot(7, 7, RED)
    sleep(5)
 