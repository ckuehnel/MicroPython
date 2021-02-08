#
# Compare internal temperature w/ temperature measured by BME280
#
# 2021-02-08 Claus Kühnel info@ckuehnel.ch
#
from machine import I2C, Pin
from bme280_float_mod import *
from utime import sleep, sleep_ms

Plotter = True

led = Pin(25, Pin.OUT)   # external LED on Pi Pico

sensor_temp = machine.ADC(4) # internal temperature sensor
conversion_factor = 3.3 / (65536)

def blink():
	led(1)
	sleep_ms(20)      # LED on for 20 milliseconds
	led(0)

sda = Pin(0)
scl = Pin(1)
i2c=I2C(0)
bme280 = BME280(i2c=i2c)

while True:
    blink()
    reading = sensor_temp.read_u16() * conversion_factor
    intTemp = 27 - (reading - 0.706)/0.001721
    extTemp = float(bme280.temperature)
    if Plotter == False:
        print('On-Chip  temperature is {:3.1f} °C'.format(intTemp))
        print('External temperature is {:3.1f} °C'.format(extTemp), end='')
        print('\t\tTemperature difference is {:3.1f} °C'.format(extTemp - intTemp))
    else:
        print(25,'On-Chip:',intTemp, 'Ext:', extTemp, 30)
    sleep(1)