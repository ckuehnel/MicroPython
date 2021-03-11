# Pi_Pico_Internals.py
# Raspberry Pi Pico connected w/ Pimoroni Pico Display
# This sample program shows some information 
# and uses some on-board resources to illustrate their query
# (c) 2021-02-04 Claus Kuehnel (info@ckuehnel.ch)
	
import machine, time, sys, uos
import picodisplay as display

from machine import Timer
from machine import Pin
from machine import ADC

led = Pin(25, Pin.OUT)   # external LED on Pi Pico
t   = Timer()

offset = ADC(0) # use grounded channel 0 for measuring ADC offset
temp   = ADC(4) # use channel 4 for measuring temperature
conversion_factor = 3.3 / (65536)

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

print('\nThis program will show some information')
print('and the usage of some on-board ressources of Raspberry Pi Pico Board\n')
print('The external led blinks ones per second\n')
print('This is a {}'.format(uos.uname().machine))
print('Installed firmware version is {}\n'.format(uos.uname().version))
print('Platform is {}'.format(sys.platform))
print('Micropython version is {}'.format(sys.version))
print('CPU frequency is {:3.0f} MHz'.format(machine.freq()/1e6))

offsetADC = offset.read_u16() * conversion_factor
print('ADC(0) offset voltage is {:3.3f} mV'.format(offsetADC * 1000))

reading = temp.read_u16() * conversion_factor
    
# The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
# Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
intTemp = 27 - (reading - 0.706)/0.001721
print('On-Chip temperature is {:3.1f} °C'.format(intTemp))

initDisplay()
width = display.get_width()
txt = '{}'.format(uos.uname().machine)
display.text(txt,10,10, width, 2)
txt = 'Firmware v.{:}'.format(uos.uname().version)
display.text(txt,10, 40, width, 2)
txt = 'Clock is {:3.0f} MHz'.format(machine.freq()/1e6)
display.text(txt,10, 85, width, 2)
txt = 'Temp is {:3.1f} *C'.format(intTemp)
display.text(txt,10, 100, width, 2)
txt = 'ADC Offset is {:3.1f} mV'.format(offsetADC * 1000)
display.text(txt,10, 115, width, 2)
display.update()

print('Press the X button for fast blinking & Y botton for slow blinking')
print('Ctrl-C stopps the running program')

global state
state = 0

while True:
    if display.is_pressed(display.BUTTON_X) == 1 and state == 0:
        print('X-Button pressed - fast blinking')
        state = 1
        t.init(period=100, mode=Timer.PERIODIC, callback = blink)
    if display.is_pressed(display.BUTTON_Y) == 1 and state == 1:
        print('Y-Button pressed - slow blinking')
        state = 0
        t.init(period=1000, mode=Timer.PERIODIC, callback = blink)
        
        