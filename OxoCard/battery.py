'''
File: battery.py

Gets voltage of OxoCard battery and controls an indicator Neopixel
2021-03-27 Claus Kühnel info@ckuehnel.ch
'''
from oxocard import *
from machine import ADC, Pin

MAX_BATTERY_VOLTAGE = 4400  # 1.1V / 100kOhm * 400kOhm
LOW_BATTERY_VOLTAGE = 3250
MIN_BATTERY_VOLTAGE = 3005

adc = ADC(Pin(34))          # create ADC object on ADC pin
#print(adc.read())           # read value, 0-4095 across voltage range 0.0v - 1.0v = 1/4 Vbat

adc.atten(ADC.ATTN_6DB)     # set 6 dB input attenuation (voltage range roughly 0.0v - 2 v)
adc.width(ADC.WIDTH_12BIT)  # set 12 bit return values (returned range 0-4095)

count = adc.read()          # read value using the newly configured attenuation and width
print(count/512)

Vbat = count*1000/512
print ('Battery Voltage = {} mV'.format(int(round(Vbat,0))))

if Vbat > LOW_BATTERY_VOLTAGE:
    dot(7, 7, GREEN)
elif Vbat >= MIN_BATTERY_VOLTAGE and Vbat <= LOW_BATTERY_VOLTAGE:
    dot(7, 7, YELLOW)
else:
    dot(7, 7, RED)
 