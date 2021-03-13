# Pi_Pico_TrafficLight.py
# Controlling Neopixel by PIO to simulate a traffic light
# using ws2812b library by benevpi
# https://github.com/benevpi/pico_python_ws2812b

import time
import ws2812b

NUM_PIX = 3  # thsi is for M5Stack RGB LED
PIN_NUM = 16
light = ws2812b.ws2812b(NUM_PIX, 0, PIN_NUM)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
COLORS = (RED, YELLOW, GREEN, BLACK)

def lights(L0, L1, L2, t):
    color = L0
    light.set_pixel(0, color[0], color[1], color[2])
    color = L1
    light.set_pixel(1, color[0], color[1], color[2])
    color = L2
    light.set_pixel(2, color[0], color[1], color[2])
    light.show()
    time.sleep(t)

while True:
    lights(RED, BLACK, BLACK, 2)
    lights(RED, YELLOW, BLACK, 1)
    lights(BLACK, BLACK, GREEN, 3)
    lights(BLACK, YELLOW, BLACK, 2) 
