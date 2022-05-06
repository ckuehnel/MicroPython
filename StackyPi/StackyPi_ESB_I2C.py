# StackyPi_ESB_I2C.py
# 
# All StackyPi_ESB_xxx.py programs are used to test single fuctions
# of the Coral Environmental Sensor Board, a Raspberry Pi HAT.
# 
# HDC2010, OPT3002, ATECC608A, BMP280 are connected to I2C0.
#
# (c) 2022-05-05 Claus Kuehnel (info@ckuehnel.ch)

from machine import Pin, I2C

i2c0 = I2C(0, scl = Pin(21), sda = Pin(20))


def printResult():
  if len(devices) == 0:
    print("No I2C device found!")
  else:
    print('{:2d} I2C device(s) found.'.format(len(devices)))
    for device in devices:  
      print('Device address: {0:3d} dec and {1:2s} hex'.format(device, hex(device)))
    
print('Scan I2C0 ...')
devices = i2c0.scan()
printResult()
