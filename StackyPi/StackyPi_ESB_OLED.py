# StackyPi_ESB_OLED.py
# 
# All StackyPi_ESB_xxx.py programs are used to test single fuctions
# of the Coral Environmental Sensor Board, a Raspberry Pi HAT.
# 
# On-board LED is connected to SPI0.
#
# (c) 2022-05-05 Claus Kuehnel (info@ckuehnel.ch)

from machine import Pin, SPI
import ssd1306
from time import sleep

spi0 = SPI(0, 10_000_000, sck=Pin(2), mosi=Pin(3), miso=Pin(4))

dc = Pin(26)   # data/command
rst = Pin(22)  # reset
cs = Pin(5)    # chip select

oled_width = 128
oled_height = 32

oled = ssd1306.SSD1306_SPI(oled_width, oled_height, spi0, dc, rst, cs)

while True:
    oled.fill(0)
    oled.text('This is', 0, 0)
    oled.text('Coral', 0, 8)
    oled.text('Environmental', 0, 16)
    oled.text('Sensor Board', 0, 24)
    oled.show()
    sleep(2)
    oled.fill(0)
    oled.text('as pHAT on', 0, 0)
    oled.text('StackyPi', 0, 8)
    oled.text('driven by', 0, 16)
    oled.text('Raspberry Pi Pico', 0, 24)
    oled.show()
    sleep(2)
