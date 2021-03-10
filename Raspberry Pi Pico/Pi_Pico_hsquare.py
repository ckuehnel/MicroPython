# Pi_Pico_hsquare.py
# MicroPython Benchmark
# http://www.robertocolistete.net/MicroPython/hsquare.zip
# Small modification 2021-03-10 Claus Kühnel info@ckuehnel.ch

from math import sqrt
import uos, sys, time

def hsquare(z,Om0,Ol,Ob):
   return (Om0+Ob)*((1+z)**3) + Ol + (1-Om0-Ol-Ob)*((1+z)**2)

def suminvsqrthsquare(numz,Om0,Ol,Ob):
    i = 0
    invnumz = 1.0/numz
    sum = 0.0
    while i < numz:
        sum += 1/sqrt(hsquare(i*invnumz,Om0,Ol,Ob))
        i += 1
    return sum

print('hsquare Benchmark for {}'.format(uos.uname().machine))
print('Installed firmware version is {}'.format(uos.uname().version))
print('Micropython version is {}'.format(sys.version))
print('CPU frequency is {:3.0f} MHz\n'.format(machine.freq()/1e6))

numz = 5*10**4

print("Doing %i calculations..." % numz)
timet1 = time.ticks_us()
suminvsqrth2 = suminvsqrthsquare(numz,0.3,0.7,0.05)
timet2 = time.ticks_us()

print("Calculations done after %u ms." %((timet2-timet1)/1000))
print("Mean time for each inverse h square calculation = %8.3f us" % (1.0*(timet2-timet1)/numz))
print("Sum of inverse h square = %15.13f" % suminvsqrth2)
print("Mean of inverse h square = %15.13f" % (suminvsqrth2/numz))

