'''
File:  bme280.py
needs: bme280_float.py

OxoCard Thermometer reads BME280 sensor and display measured temperature on matrix display
2021-03-27 Claus Kühnel info@ckuehnel.ch
'''
from oxocard import *
from machine import Pin, I2C, ADC

i2c = I2C(scl = Pin(22), sda = Pin(21))

from bme280_float import *
from utime import sleep

#bme280 = BME280(i2c=i2c)
bme280 = BME280(i2c=i2c, mode=BME280_OSAMPLE_8, address=BME280_I2CADDR)

def getBattery():
    MAX_BATTERY_VOLTAGE = 4400  # 1.1V / 100kOhm * 400kOhm
    LOW_BATTERY_VOLTAGE = 3250
    MIN_BATTERY_VOLTAGE = 3005

    adc = ADC(Pin(34))          # create ADC object on ADC pin
    adc.atten(ADC.ATTN_6DB)     # set 6 dB input attenuation (voltage range roughly 0.0v - 2 v)
    adc.width(ADC.WIDTH_12BIT)  # set 12 bit return values (returned range 0-4095)

    count = adc.read()          # read value using the newly configured attenuation and width
    Vbat = count*1000/512
    print ('Battery Voltage = {} mV'.format(int(round(Vbat,0))))

    if Vbat > LOW_BATTERY_VOLTAGE:
        dot(7, 7, GREEN)
    elif Vbat >= MIN_BATTERY_VOLTAGE and Vbat <= LOW_BATTERY_VOLTAGE:
        dot(7, 7, YELLOW)
    else:
        dot(7, 7, RED)
  
clear()
dim(30)

while True:
    temp = bme280.read_compensated_data()[0]
    print('Temperature = {} °C'.format(round(temp, 1)))
    display(round(temp, 0))
    getBattery()
    print()
    sleep(15)

