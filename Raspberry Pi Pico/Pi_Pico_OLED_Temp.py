# Pi_Pico_OLED_Temp.py
3
# Compare internal temperature w/ temperature measured by BME280 
# and display results on OLED and Console
#
# 2021-02-08 Claus Kühnel info@ckuehnel.ch
#
from machine import I2C, Pin
from bme280_float_mod import *
from utime import sleep, sleep_ms
import ssd1306

led = Pin(25, Pin.OUT)   # external LED on Pi Pico

sensor_temp = machine.ADC(4) # internal temperature sensor
conversion_factor = 3.3 / (65536)

def blink():
	led(1)
	sleep_ms(20)      # LED on for 20 milliseconds
	led(0)

# Display size
oled_width = 128
oled_height = 64

# Pi Pico assignement
sda=Pin(0)
scl=Pin(1)

i2c=I2C(0)
bme280 = BME280(i2c=i2c)
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.text('Thermometer', 0, 20) 
oled.text('using BME280 and', 0, 30)
oled.text('on-chip sensor', 0,40)
oled.show()
sleep(2)
oled.fill(0)
oled.show()


while True:
    blink()
    reading = sensor_temp.read_u16() * conversion_factor
    intTemp = 27 - (reading - 0.706)/0.001721
    extTemp = float(bme280.temperature)
    
    print('On-Chip  temperature is {:3.1f} °C'.format(intTemp))
    print('External temperature is {:3.1f} °C'.format(extTemp), end='')
    print('\t\tTemperature difference is {:3.1f} °C'.format(extTemp - intTemp))
    
    oled.fill(0)
    oled.show()
    
    unit = ' *C'
    msg = 'BME280  ' + str(round(extTemp, 1)) + unit 
    oled.text(msg, 0, 20)
    msg = 'On-Chip ' + str(round(intTemp, 1)) + unit
    oled.text(msg, 0, 30)
    msg = 'Delta   ' + str(round((extTemp- intTemp), 1)) + unit
    oled.text(msg, 0, 45)
    oled.show()
    sleep(10)