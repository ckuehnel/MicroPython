# sgp30_simpletest.py
# https://github.com/alexmrqt/micropython-sgp30
# adaption to the I2C bus of Raspberry Pi Pico by
# 2021-03-11 Claus Kühnel info@ckuehnel.ch

"""
Example for using the SGP30 with MicroPython and the Adafruit library.

Uses instructions from "SGP30 Driver Integration (for Software I²C)" to handle
self-calibration of the sensor:
    - if no baseline found, wait 12h before storing baseline,
    - if baseline found, store baseline every hour.

Baseline is writen in co2eq_baseline.txt and tvoc_baseline.txt.

Note that if the sensor is shut down during more than one week, then baselines
must be manually deleted.
"""

import time
from machine import Pin, I2C
import adafruit_sgp30

# Initialize I2C bus
sda=Pin(0)
scl=Pin(1)
i2c=I2C(0,sda=sda, scl=scl, freq=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])

# Initialize SGP-30 internal drift compensation algorithm.
sgp30.iaq_init()

# Wait 15 seconds for the SGP30 to properly initialize
print("Waiting 15 seconds for SGP30 initialization.")
time.sleep(15)

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

    #A measurement should be done every 60 seconds, according to the doc.
    time.sleep(1)

