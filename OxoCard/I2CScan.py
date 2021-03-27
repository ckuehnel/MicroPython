'''
File:  I2CScan.py

Scans I2C bus of OxoCard and prints conencted devices
2021-03-27 Claus Kühnel info@ckuehnel.ch
'''
from oxocard import *
from machine import Pin, I2C

i2c = I2C(scl = Pin(22), sda = Pin(21))

def printResult():
  if len(devices) == 0:
    print("No I2C device found!")
  else:
    print('{:2d} I2C device(s) found.'.format(len(devices)))
    for device in devices:  
      print('Device address: {0:3d} dec and {1:2s} hex'.format(device, hex(device)))
    
print('Scan I2C ...')
devices = i2c.scan()
printResult()
