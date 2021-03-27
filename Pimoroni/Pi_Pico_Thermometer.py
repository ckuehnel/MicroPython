# Pi_Pico_Thermometer.py
# Raspberry Pi Pico connected w/ Pimoroni Pico Display
# Using the internal temperature sensor connected to ADC(4) for measuring 
# ambient temperature in a simple way.
# The temperature sensor measures the Vbe voltage of a biased bipolar diode.
# Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
# 
# (c) 2021-02-05 Claus Kuehnel (info@ckuehnel.ch)

import machine, time
import picodisplay as display

from machine import Timer
from machine import Pin

led = Pin(25, Pin.OUT)   # external LED on Pi Pico
t   = Timer()

sensor_temp = machine.ADC(4) # internal temperature sensor
conversion_factor = 3.3 / (65536)

# Thermostat Range (set your limits here)
# OverTemp  > 30  -> LED red
# Normal   28..30 -> LED green
# Under     < 28  -> LED blue 
UL = 30 # Upper Limit
LL = 28 # Lower Limit

def blink(Timer):
	led(1)
	time.sleep_ms(20)      # LED on for 20 milliseconds
	led(0)

def initDisplay():
    width = display.get_width()
    height = display.get_height()

    display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
    display.init(display_buffer)
    display.set_backlight(1)

    display.set_pen(0, 0, 0)    # black
    display.clear()
    display.set_pen(100, 100, 100) # white

t.init(period=1000, mode=Timer.PERIODIC, callback = blink)

initDisplay()
width = display.get_width()

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    intTemp = 27 - (reading - 0.706)/0.001721
    print('On-Chip temperature is {:3.1f} °C'.format(intTemp))
    display.set_pen(0, 0, 0)    # black
    display.clear()
    display.set_pen(128, 128, 128) # white
    txt = 'Temp {:3.1f} *C'.format(intTemp)
    display.text(txt,10, 55, width, 4)
    display.update()
    if   intTemp > UL: display.set_led(128, 0, 0)
    elif intTemp < LL: display.set_led(0, 0, 128)
    else: display.set_led(0, 128, 0)
    time.sleep(5)
    