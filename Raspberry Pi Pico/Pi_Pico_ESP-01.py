# Pi_Pico_ESP-01.py
# Based on mpyPico_ESP-01S_20210219a.py
# http://helloraspberrypi.blogspot.com/2021/02/connect-esp-01s-esp8266-to-raspberry-pi.html

# Connections
# Pi_Pico 3V3 3V3   GND  GPIO4 GPIO5
# ESP-01  VCC CH_PD GND  RX    TX

import uos, machine, utime

"""
ESPRESSIF AT Command Set
https://docs.espressif.com/projects/esp-at/en/latest/AT_Command_Set/
"""

print('Pi Pico WiFi connection by ESP-01')
print("\nMachine: \t" + uos.uname()[4])
print("MicroPython: \t" + uos.uname()[3] + "\n")

#indicate program started visually
led_onboard = machine.Pin(25, machine.Pin.OUT)
led_onboard.value(0)     # onboard LED OFF/ON for 0.5/1.0 sec
utime.sleep(0.5)
led_onboard.value(1)
utime.sleep(1.0)
led_onboard.value(0)

uart1 = machine.UART(1, baudrate=9600)
print(uart1)

def sendCMD_waitResp(cmd, uart=uart1, timeout=1000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(uart, timeout)
    print()
    
def waitResp(uart=uart1, timeout=1000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)
    
sendCMD_waitResp('AT\r\n')          #Test AT startup
sendCMD_waitResp('AT+GMR\r\n')      #Check version information
#sendCMD_waitResp('AT+RESTORE\r\n') #Restore Factory Default Settings
sendCMD_waitResp('AT+CWMODE?\r\n')  #Query the Wi-Fi mode
sendCMD_waitResp('AT+CWMODE=1\r\n') #Set the Wi-Fi mode = Station mode
sendCMD_waitResp('AT+CWMODE?\r\n')  #Query the Wi-Fi mode again
sendCMD_waitResp('AT+CWLAPOPT=1,2047\r\n') #Set order in AP list
sendCMD_waitResp('AT+CWLAP\r\n', timeout=5000) #List available APs
sendCMD_waitResp('AT+CWDHCP_DEF=1,1\r\n') #Enables DHCP
sendCMD_waitResp('AT+CWJAP="Sunrise_2.4GHz_8AC2A0","u2u7fgzv31Ds"\r\n', timeout=5000) #Connect to AP
sendCMD_waitResp('AT+CIPMUX=1\r\n', timeout=5000) #Set Multiple TCP Connections
sendCMD_waitResp('AT+CIFSR\r\n', timeout=5000)    #Obtain the Local IP Address
sendCMD_waitResp('AT+CIPSTATUS\r\n') #Get the Connection Status 
sendCMD_waitResp('AT+PING="www.ckuehnel.ch"\r\n', timeout=2000) #Ping a website






    
