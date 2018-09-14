#!/usr/bin/python
import spidev
import time
import os
import sys
import RPi.GPIO as GPIO

#Define Variables
global count
count = 0
timer = 0
start = True
global delay
delay = 0.5
ldr_channel = 0
temp_channel = 1
pot_channel = 2
resetSwitch = 17
StopSwitch = 27
dispSwitch = 22
freqSwitch = 18
arr = []
#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
GPIO.setmode(GPIO.BCM)
# switch 1,2,3,4
GPIO.setup(resetSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(StopSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dispSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(freqSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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


def Temperature (voltage):
    temp = voltage
    temp = int ((temp - 0.5)/0.01 )
    return temp

def Percent (voltage):
    percentage = (int (voltage/3.1*100))
    return percentage

# function definition: threaded callback
def resetCallback(channel):
    
    timer = 0
    print ("\n" * 100)

def stopCallback(channel):
    global count
    arr.clear()
    count += 1
    if (count%2 == 0):
        start = True
        print("Start")
    else:
        start = False
        print("Stop")

def freqCallback(channel):
    global delay
    if (delay >= 2):
        delay = 0.5
        print(delay)
    else:
        delay = delay * 2
        print(delay)

def displayCallback(channel):
    print('_______________________________________________')
    print('Time        Timer          Pot    Temp   Light')

    for i in range(0,5):
        print(arr[i])
        print('_____________________________________________')

# 'bouncetime=200' includes the bounce control
# ‘bouncetime=200’ sets 200 milliseconds during which second button press will
# to remove: GPIO.remove_event_detect(port_number)
# Under a falling-edge detection, regardless of current execution
# callback function will be called

GPIO.add_event_detect(resetSwitch, GPIO.FALLING, callback=resetCallback,bouncetime=200)
GPIO.add_event_detect(StopSwitch, GPIO.FALLING, callback=stopCallback,bouncetime=200)
GPIO.add_event_detect(dispSwitch, GPIO.FALLING, callback=displayCallback,bouncetime=200)
GPIO.add_event_detect(freqSwitch, GPIO.FALLING, callback=freqCallback,bouncetime=200)
try:
    while True:
        if (start == True):
            pot_data = GetData (pot_channel)
            pot_volts = ConvertVolts(pot_data ,2)
            ldr_data = GetData (ldr_channel)
            ldr_volts = ConvertVolts(ldr_data ,2)
            temp_data = GetData (temp_channel)
            temp_volts = ConvertVolts(temp_data ,2)
            temp = Temperature(temp_volts)
            light = Percent(ldr_volts)
            element = (str(time.strftime("%H:%M:%S   ")) + '00:00:' + str(timer)+ "     " + str(pot_volts)+ 'V    ' + str(temp) + 'C     ' + str(light) +'%')
            # print (time.strftime("%H:%M:%S  "),'00:00:' + str(timer),'   ',str(pot)+ 'V   ' , str(temp) + 'C   ', str(light) +'%')
            arr.append(element)

 # Wait before repeating loop
        time.sleep(delay)
        timer +=delay
except KeyboardInterrupt:
    spi.close()
