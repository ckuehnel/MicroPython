# StackyPi_SPI.py
# 
# This sample program uses SPI on header & SD card

# (c) 2021-02-04 Claus Kuehnel (info@ckuehnel.ch)

from machine import Pin, SPI
import binascii

spi0 = SPI(0, 10_000_000, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
spi1 = SPI(1, 10_000_000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))

print("StackyPi SPI Test")
print("connect Pin19 and Pin21 on Header for SPI0")

spiOut = bytearray([0xA5, 0x5A])      # create a buffer
spiIn  = bytearray([0x00, 0x00])      # create a buffer

print("before SPI0 transfer")
#print(spiOut)
print(", ".join(hex(b) for b in spiOut))
#print(spiIn)
print(", ".join(hex(b) for b in spiIn))

spi0.write_readinto(spiOut, spiIn)
print("after SPI0 transfer")
#print(spiOut)
print(", ".join(hex(b) for b in spiOut))
#print(spiIn)
print(", ".join(hex(b) for b in spiIn))