# Pi_Pico_I2CScan.py
# Scan both I2C-Busses for connected devices
# I2C0: SDA = GPIO0,  SCL = GPIO1
# I2C1: SDA = GPIO14, SCL = GPIO15
# 2021-03-11 Claus Kühnel info@ckuehnel.ch

from machine import Pin, I2C

sda0=Pin(0)
scl0=Pin(1)
i2c0=I2C(0,sda=sda0, scl=scl0, freq=400000)

sda1=Pin(14)
scl1=Pin(15)
i2c1=I2C(1,sda=sda1, scl=scl1, freq=400000)

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

print('\nScan I2C1 ...')
devices = i2c1.scan()
printResult()