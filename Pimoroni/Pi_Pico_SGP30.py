# Pi_Pico_SGP30.py
# Measuring air quality by Sensirion SGP30 and display
# results on Pimoroni Pico Display
# based on https://github.com/alexmrqt/micropython-sgp30
# 2021-03-11 Claus Kühnel info@ckuehnel.ch

import machine, time, uos
from machine import Pin, I2C
import adafruit_sgp30
import picodisplay as display

# Initialize I2C bus
sda=Pin(0)
scl=Pin(1)
i2c=I2C(0,sda=sda, scl=scl, freq=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

def clearDisplay():
    display.set_pen(0, 0, 0)    # black
    display.clear()
    display.set_pen(100, 100, 100) # white

def initDisplay():
    width = display.get_width()
    height = display.get_height()

    display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
    display.init(display_buffer)
    display.set_backlight(1)
    clearDisplay()

def showLED(val):
    if val < 800:
        display.set_led(0, 128, 0) # Green
    if val >= 800 and val < 1200:
        display.set_led(241, 196, 15) #Yellow
    if val >= 1200:
        display.set_led(255, 0, 0)  # Red

    
print('\nThis program measures air quality by Sensirion SGP30')
print('and displays results on Pimoroni Pico Display using Raspberry Pi Pico Board\n')
print('Installed firmware version is {}\n'.format(uos.uname().version))

initDisplay()
width = display.get_width()
txt = 'Air Quality by SGP30'
display.text(txt,10, 10, width, 3)

# Initialize SGP-30 internal drift compensation algorithm.
sgp30.iaq_init()

# Wait 15 seconds for the SGP30 to properly initialize
print("Waiting 15 seconds for SGP30 initialization.")
txt = 'Waiting 15 seconds...'
display.text(txt,10, 60, width, 2)
display.update()
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
    
    clearDisplay()
    txt = 'Air Quality by SGP30'
    display.text(txt,10, 10, width, 3)
    txt = 'eCO2: {} ppm'.format(co2eq)
    display.text(txt,10, 60, width, 3)
    txt = 'TVOC: {} ppm'.format(tvoc)
    display.text(txt,10, 90, width, 3)
    showLED(co2eq)
    display.update()
    
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

