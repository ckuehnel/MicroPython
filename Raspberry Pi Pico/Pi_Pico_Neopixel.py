# Pi_Pico_Neopixel.py
# Controlling Neopixel by PIO to simulate a traffic light
# based on http://www.pibits.net/code/raspberry-pi-pico-and-neopixel-example-in-micropython.php

import array, time
from machine import Pin
import rp2
 
# Configure the number of WS2812 LEDs, pins and brightness.
NUM_LEDS = 3
PIN_NUM = 16
brightness = .1
 
 
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()
 
 
# Create the StateMachine with the ws2812 program, outputting on Pin(16).
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))
 
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)
 
# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])
 
def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)
 
def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]
 
def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)

# Phases for traffic light
def lights(L0, L1, L2, t):
    pixels_set(0, L0)
    pixels_set(1, L1)
    pixels_set(2, L2)
    pixels_show()
    time.sleep(t)
    
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
 
while True:      # Traffic light sequence
    lights(RED, BLACK, BLACK, 3)
    lights(RED, YELLOW, BLACK, 1)
    lights(BLACK, BLACK, GREEN, 3)
    lights(BLACK, YELLOW, BLACK, 2) 