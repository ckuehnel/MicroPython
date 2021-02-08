from bme680 import *
from machine import I2C, Pin
import utime

sda = Pin(0)
scl = Pin(1)
bme = BME680_I2C(I2C(0, sda=sda, scl = scl))

# And a short delay to wait until the I2C port has finished activating.
utime.sleep_ms(100)

while True:
    print(bme.temperature, bme.humidity, bme.pressure, bme.gas)
    utime.sleep(1)

