'''
File:  SGP30.py
needs: adafruit_sgp30.py

Measuring air quality by Sensirion SGP30 and display results on OxoCard matrix display
based on https://github.com/alexmrqt/micropython-sgp30
2021-03-27 Claus Kühnel info@ckuehnel.ch
'''

from oxocardext import *
import machine, time, uos
from machine import Pin, I2C
import adafruit_sgp30

i2c = I2C(scl = Pin(22), sda = Pin(21))

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

def showLED(val):
    if val < 800:
        fillRectangle(3, 3, 2, 2, GREEN)
    if val >= 800 and val < 1200:
        fillRectangle(2, 2, 4, 4, YELLOW)
    if val >= 1200:
        fillRectangle(0, 0, 8, 8, RED)
    
print('\nThis program measures air quality by Sensirion SGP30')
print('and displays results on OxoCard Matrix\n')
print('Installed firmware version is {}\n'.format(uos.uname().version))

# Blue dot means initializing
clear()
dot(3, 3, BLUE)

# Initialize SGP-30 internal drift compensation algorithm.
sgp30.iaq_init()

# Wait 15 seconds for the SGP30 to properly initialize
print("Waiting 15 seconds for SGP30 initialization.")
i = 15
while i > 0:
    i -=1
    print(i)
    line(4, 3, 5, 2, BLACK)
    line(3, 3, 7, 2, BLUE) 
    time.sleep_ms(500)
    line(3, 3, 7, 2, BLACK)
    line(4, 3, 5, 2, BLUE)
    time.sleep_ms(500)
        
# Retrieve previously stored baselines, if any (helps the compensation algorithm).
has_baseline = False
try:
    f_co2 = open('co2eq_baseline.txt', 'r')
    f_tvoc = open('tvoc_baseline.txt', 'r')

    co2_baseline = int(f_co2.read())
    tvoc_baseline = int(f_tvoc.read())
    
    #Use them to calibrate the sensor
    sgp30.set_iaq_baseline(co2_baseline, tvoc_baseline)

    f_co2.close()
    f_tvoc.close()

    has_baseline = True
except:
    print('Impossible to read SGP30 baselines!')

#Store the time at which last baseline has been saved
baseline_time = time.time()

while True:
    co2eq, tvoc = sgp30.iaq_measure()
    print('co2eq = ' + str(co2eq) + ' ppm \t tvoc = ' + str(tvoc) + ' ppb')
    
    clear()
    showLED(co2eq)
    
    # Baselines should be saved after 12 hour the first timen then every hour,
    # according to the doc.
    if (has_baseline and (time.time() - baseline_time >= 3600)) \
            or ((not has_baseline) and (time.time() - baseline_time >= 43200)):

        print('Saving baseline!')
        baseline_time = time.time()

        try:
            f_co2 = open('co2eq_baseline.txt', 'w')
            f_tvoc = open('tvoc_baseline.txt', 'w')

            bl_co2, bl_tvoc = sgp30.get_iaq_baseline()
            f_co2.write(str(bl_co2))
            f_tvoc.write(str(bl_tvoc))

            f_co2.close()
            f_tvoc.close()

            has_baseline = True
        except:
            print('Impossible to write SGP30 baselines!')

    #A measurement should be done every 10 seconds, according to the doc.
    time.sleep(10)

