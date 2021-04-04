'''
File:  RoomConditionMonitor.py
needs: adafruit_sgp30.py

This Room Condition Monitor running on OxoCard is using
SHT30 to measure temperature and humidity and
SGP30 to measure TVOC and eCO2.
Measured values are displayed on 0.96" OLED and air quality
is display as pattern on OxoCard matrix display.

2021-03-27 Claus Kühnel info@ckuehnel.ch
'''

from oxocardext import *
from machine import Pin, I2C
from oled import Oled
import time
import adafruit_sgp30

# Initialize I2C bus
i2c = I2C(scl = Pin(22), sda = Pin(21))

#Initialize OLED
oled = Oled()

# Create library object on I2C bus
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

# Retrieve previously stored baselines, if any (helps the compensation algorithm).
has_baseline = False
baseline_time = 0

#Read sensor values from SHT30
def readSHT30():
    buf = bytearray(2)
    buf[0] = 0x30
    buf[1] = 0xA2
    i2c.writeto(0x44, buf)
    time.sleep_ms(100)

    buf2 = bytearray(6)
    buf[0] = 0x2c
    buf[1] = 0x06
    i2c.writeto(0x44, buf)
    time.sleep_ms(100)
    
    buf2 = i2c.readfrom(0x44, 6)

    temp_raw = (buf2[0] << 8) + (buf2[1])
    humi_raw = (buf2[3] << 8) + (buf2[4])
    temp = round((175 * temp_raw / 65535 - 45), 1)
    humi = round((100 * humi_raw / 65535), 1)
     
    print('temp  = ' + str(temp) + ' °C   \t humi = ' + str(humi) + ' %rH')
    oled.text('Temp = ' + str(temp) + ' *C', 0, 12)
    oled.text('Humi = ' + str(humi) + ' %rH', 0, 24)

#LED pattern for air quality indicator
def showLED(val):
    if val < 800:
        fillRectangle(3, 3, 2, 2, GREEN)
    if val >= 800 and val < 1200:
        fillRectangle(2, 2, 4, 4, YELLOW)
    if val >= 1200:
        fillRectangle(1, 1, 6, 6, RED)

def initSGP30():
    # Initialize SGP-30 internal drift compensation algorithm.
    sgp30.iaq_init()
    clear()
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
    global has_baseline
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
    global baseline_time
    baseline_time = time.time()
    
def readSGP30():
    co2eq, tvoc = sgp30.iaq_measure()
    print('co2eq = ' + str(co2eq) + ' ppm \t tvoc = ' + str(tvoc) + ' ppb')
    
    oled.text('TVOC = ' + str(tvoc) + ' ppb', 0, 36)
    oled.text('eCO2 = ' + str(co2eq) + ' ppm', 0, 48)
    
    clear()
    showLED(co2eq)
    
    # Baselines should be saved after 12 hour the first timen then every hour,
    # according to the doc.
    global has_baseline
    global baseline_time
    if (has_baseline and (time.time() - baseline_time >= 3600)) or ((not has_baseline) and (time.time() - baseline_time >= 43200)):
        print('Saving baseline!')
        baseline_time = time.time()

        try:
            f_co2 = open('co2eq_baseline.ttime.sleep(10)xt', 'w')
            f_tvoc = open('tvoc_baseline.txt', 'w')

            bl_co2, bl_tvoc = sgp30.get_iaq_baseline()
            f_co2.write(str(bl_co2))
            f_tvoc.write(str(bl_tvoc))

            f_co2.close()
            f_tvoc.close()

            has_baseline = True
        except:
            print('Impossible to write SGP30 baselines!')


print('\nThis program is using SHT30 to measure temperature and humidity')
print('and SGP30 to measure TVOC and eCO2.')
print('Measured values are displayed on 0.96" OLED and air quality')
print('is display as pattern on OxoCard matrix display.\n')
print('Installed firmware version is {}\n'.format(uos.uname().version))

oled.text('Air Cond Monitor', 0, 0)
oled.text('Initializing', 0, 24)
oled.text('SGP30 sensor...', 0, 36)
oled.show()
initSGP30()

while True:
    oled.fill(0) # clears frame buffer
    oled.text('Air Cond Monitor', 0, 0)
    readSHT30()
    readSGP30()
    oled.show()
    print()
    time.sleep(10)