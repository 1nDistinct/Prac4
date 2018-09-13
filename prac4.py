#!/usr/bin/python

import spidev
import time
import os
import sys
import RPi.GPIO as GPIO
import Adafruit_MCP3008



#Define Variables
values = [0]*8
delay = 0.5
ldr_channel = 0
temp_channel = 1
pot_channel = 2
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
switch_1 = 17
switch_2 = 27
switch_3 = 22
mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI,
miso=SPIMISO)
#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)

GPIO.setmode(GPIO.BCM)

# switch 1 & switch 2: input – pull-up
GPIO.setup(switch_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# switch 3: input – pull-down
GPIO.setup(switch_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# pin definition
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

def GetData(channel): # channel must be an integer 0-7
    adc = spi.xfer2([1,(8+channel)<<4,0]) # sending 3 bytes
    data = ((adc[1]&3) << 8) + adc[2]
    return data

# function to convert data to voltage level,
# places: number of decimal places needed
def ConvertVolts(data,places):
    volts = (data * 3.3) / float(1023)
    volts = round(volts,places)
    return volts

def printData():
    for i in range(8):
        values[i] = mcp.read_adc(i)
 # delay for a half second
    time.sleep(0.5)
    print values

# function definition: threaded callback
def callback1(channel):

def callback2(channel):
# put code here

try:
    while True:




        # Under a falling-edge detection, regardless of current execution
# callback function will be called
        GPIO.add_event_detect(switch_1, GPIO.FALLING, callback=callback1,
        bouncetime=200)
        GPIO.add_event_detect(switch_2, GPIO.FALLING, callback=callback2,
        bouncetime=200)
# 'bouncetime=200' includes the bounce control
# ‘bouncetime=200’ sets 200 milliseconds during which second button press will
# to remove: GPIO.remove_event_detect(port_number)
        try:
            GPIO.wait_for_edge(switch_3, GPIO.RISING)
        except KeyboardInterrupt:
            GPIO.cleanup() # clean up GPIO on CTRL+C exit

        GPIO.cleanup() # clean up GPIO on normal exit

        # Read Voltage data
        pot_data = GetData (pot_channel)
        ldr_data = GetData (ldr_channel)
        temp_data = GetData (temp_channel)
        sensor_volt = ConvertVolts(sensor_data,2)
 # Wait before repeating loop
        time.sleep(delay)
    except KeyboardInterrupt:
        spi.close()
