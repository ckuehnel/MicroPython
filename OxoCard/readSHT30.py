'''
File:  readSHT30.py
needs: none
based on https://www.wemos.cc/en/latest/tutorials/w600/get_started_with_micropython_w600.html#i2c

Reads SHT30 sensor and prints temperature and humidity
2021-03-27 Claus Kühnel info@ckuehnel.ch
'''

from oxocard import *
from machine import Pin, I2C
import time

i2c = I2C(scl = Pin(22), sda = Pin(21))

def readSHT30():
    buf = bytearray(2)
    buf[0] = 0x30
    buf[1] = 0xA2
    i2c.writeto(0x44, buf)
    time.sleep_ms(100)

    buf2 = bytearray(6)
    buf[0] = 0x2c
    buf[1] = 0x06
    i2c.writeto(0x44, buf)
    time.sleep_ms(100)
    
    buf2 = i2c.readfrom(0x44, 6)

    temp_raw = (buf2[0] << 8) + (buf2[1])
    humi_raw = (buf2[3] << 8) + (buf2[4])
    temp = 175 * temp_raw / 65535 - 45
    humi = 100 * humi_raw / 65535
        
    return temp, humi

temp, humi = readSHT30()
print('Temperature = {} °C'.format(round(temp,1)))
print('Humidity    = {} %rH'.format(round(humi, 1)))