# Read BME280 sensor and display data on pico explorer LCD
# 2021-02-17 Claus Kuehnel info@ckuehnel.ch

from machine import Pin, I2C
from time import sleep
import BME280
#import Piezo

# Pico Explorer boilerplate
import picoexplorer as display
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)

sda=Pin(20)         # Pico Explorer
scl=Pin(21)
i2c=I2C(0,sda=sda, scl=scl, freq=400000)
bme = BME280.BME280(i2c=i2c)

def clear():                        # this function clears Pico Explorer's screen to black
    display.set_pen(0,0,0)
    display.clear()
    display.update()
    
clear()
display.set_pen(0, 255, 0)
display.text('Weather Station', 0, 100, width, 3)
display.update()
# Piezo.playsong(Piezo.song)
sleep(2)
    

while True:
  temp = bme.read_temperature()/100
  hum = bme.read_humidity()/1000
  pres = bme.read_pressure()/25600
  
  print('Temperature: {:.1f} °C'.format(temp))
  print('Humidity:    {:.1f} %rH'.format(hum))
  print('Pressure:    {:.0f} hPa'.format(pres))
  print("")
  
  # writes the reading as text
  clear()
  display.set_pen(0, 255, 0)
  display.text('Temp: {:.1f} *C'.format(temp), 10, 60, width, 3)
  display.text('Humi: {:.1f} %rH'.format(hum), 10, 100, width, 3)
  display.text('Pres: {:.0f} hPa'.format(pres), 10,140, width, 3)
    
  # time to update the display
  display.update()
  

  sleep(5)
    

