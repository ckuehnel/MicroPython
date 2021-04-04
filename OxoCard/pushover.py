'''
File:  pushover.py
needs: tcpcom, oxocard, oxobutton, machine, time
based on https://www.tigerjython4kids.ch/index.php?inhalt_links=robotik/navigation.inc.php&inhalt_mitte=robotik/iot/push.inc.php

Reads SHT30 sensor and prints temperature and humidity to matrix display and sends pushover message
2021-04-03 Claus Kühnel info@ckuehnel.ch
'''
from tcpcom import Wlan, HTTPClient
from oxocard import *
from oxobutton import *
from machine import Pin, I2C
from time import sleep
from credentials import SSID, PASS, apitoken, userkey

Wlan.connect(SSID, PASS)

i2c = I2C(scl = Pin(22), sda = Pin(21))

title =  'Oxocard Room Conditions'

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

dim(10) # reduce brightness of Neopixel

while True:
    temp, humi = readSHT30()
    display(int(temp + 0.5))
    sleep(3)
    display(int(humi + 0.5))
    sleep(3)
    message = "Temperature: %4.1f degC\n" %temp
    message += "Humidity: %4.1f%%rH" %humi
    smallTextScroll('Send message...', BLUE, BLACK, 8)
    HTTPClient.pushover(apitoken, userkey, title, message)
    clear()
    dot(3, 3, GREEN)
    sleep(60 * 15)


