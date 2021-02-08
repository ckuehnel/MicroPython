#
# Test BMx280 Breakout Board
# Cheap boards equipped with BMP280 or BME280 are offered and you can't
# see which sensor is on board. You can use this program to test it.
# BMP280 measures temperature and barometric pressure only, no humidity.
# The sensors can be differentiated using the DevideID
#
# 2021-02-08 Claus Kühnel info@ckuehnel.ch
#
from machine import I2C, Pin
from bme280_float_mod import *
from utime import sleep

sda = Pin(0)
scl = Pin(1)
i2c=I2C(0)
bme280 = BME280(i2c=i2c)

while True:
    if bme280.isBME280: print(bme280.values)
    else: print(bme280.BMP280_values) # no humidity when BMP280
    sleep(1)
