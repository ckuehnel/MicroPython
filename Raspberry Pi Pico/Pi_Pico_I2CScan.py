from machine import Pin, I2C

sda=Pin(0)
scl=Pin(1)
i2c=I2C(0,sda=sda, scl=scl, freq=400000)

devices = i2c.scan()

if len(devices) == 0:
  print("No I2C device found!")
else:
  print('{:2d} I2C device(s) found.'.format(len(devices)))

  for device in devices:  
    print('Device address: {0:3d} dec and {1:2s} hex'.format(device, hex(device)))
    
    