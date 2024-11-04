############################################################################
# Dynamic Speed Limit System (CMPE2965 Project)
# Russel Carpio & John Tayag 
# 4/8/2024
#
# Project Description :
# Base Code to use for the "DSLS" with functions to control 8x8 matrix displays
# and Oled displays and also code that will take data from speed and
# temperature sensors which will be sent to a database through wifi connection
############################################################################
#--------------------------------IMPORTS-----------------------------------#
############################################################################
from machine import Pin, SPI , I2C, ADC, PWM, RTC
import max7219
from ssd1306 import SSD1306_I2C
from time import sleep_ms, ticks_diff, ticks_ms, sleep
#from datetime import datetime

from PWMCounter import PWMCounter

import bme280
import urllib
import network
import math
import random

############################################################################
#----------------------------------SETUP-----------------------------------#
############################################################################
led = machine.Pin("LED", machine.Pin.OUT)

# Set PWM to output test signal
pwm = PWM(Pin(0))
pwm.duty_u16(1 << 15)
pwm.freq(8000)

# Configure counter to count rising edges on GP15
counter = PWMCounter(15, PWMCounter.EDGE_RISING)
# Set divisor to 1 (just in case)
counter.set_div()
# Start counter
counter.start()

# Set sampling time in ms
sampling_time = 150 #150
last_check = ticks_ms()

adc = ADC(Pin(26)) # Sets ADC as pin 26

spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=1,
                  phase=1,
                  bits=8,
                  sck=machine.Pin(2), # sets sck to pin 2
                  mosi=machine.Pin(3)) # sets mosi (DIN) to pin 3
cs = Pin(5, Pin.OUT) # sets chip select (CS) to pin 5

si2c=I2C(0,scl=Pin(9),sda=Pin(8),freq=200000)
i2c=I2C(1,scl=Pin(7),sda=Pin(6),freq=400000)

############################################################################
#---------------------------------FUNCTIONS--------------------------------#
############################################################################
def flicker(time):
    """
    Flicker is function to "flicker" the led over a specified time
    
    arg : time
    return : none
    """
    for x in range(int(time)):
        led.toggle()
        sleep(1)

def connect_to_wifi(ssid, psk):
    """
    Will try to connect to wifi when given an ssid, psk
    will light led as an indicator that wifi is connected
    otherwise will throw when failed to connect
    
    arg : ssid,psk
    return : none
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)
    
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect")
        flicker(10)
    if not wlan.isconnected():
        led.off()
        raise Exception("Wifi not available")
    print("Connected to Wifi")
    led.on()

def insertOne(temp, hum, avgSpeed, rainVal, DFPoint, time):
    try:
        url = "https://us-east-2.aws.data.mongodb-api.com/app/data-sxowy/endpoint/data/v1/action/insertOne"
        headers = { "api-key": "FU8kppU9XuZpgoRxGdAzTM1BftH9MgSGMGRdsToCSP9p2nVqpIka4HcfQHvbx27r" }
        
        data = {"temp": temp,
                "humidity": hum,
                "avgSpeed": avgSpeed,
                "rainVal": rainVal,
                "dFPoint": DFPoint,
                "createdAt": time
                }
        
        payload = {
            "dataSource": "Cluster0",
            "database": "test",
            "collection": "weathers",
            "document": data,
        }
        
        response = urllib.urlopen(url=url, json=payload, headers=headers)
        
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        
        if response.status_code == 201:
            print("success")
        else:
            print("Error")
        
        response.close()
        
    except Exception as e:
        print(e)
        
def FreqToSpeed(RFreq):
    RecievedFreq = float(RFreq)
    
    #sSound = 332 + (0.61 * Temp)  # Speed of sound based on temperature
    #Speed = round((-SensorFreq * sSound + (sSound * RecievedFreq)) / RecievedFreq, 2)  # Using Doppler Effect formula
    Speed = RecievedFreq/47 #Changed from 44 to offset capture time
    return Speed
    
def calculateNewSpeed(temperature, relativeHumidity, medianSpeed, rainVal):
#     global baseSpeedLimit
    baseSpeedLimit = 110
    # Temporary placeholder for rounded speed limit.
    roundedSpeedLimit = baseSpeedLimit
    reducedSpeedLimit = 0

    # If temperature is at frost point (where relative humidity = 100 and temperature < 0)
    # reduce base speed limit by 10%.
    # Temperature is comprared to -7 instead of 0 to account for difference between air and road temperature and accuracy of the sensor.
    if rainVal <= 35000:
        reducedSpeedLimit = baseSpeedLimit * 0.85
        roundedSpeedLimit = floorToNearest5(reducedSpeedLimit)

    elif relativeHumidity == 100 and temperature < -7 or 45000 > rainVal > 35000:
        reducedSpeedLimit = baseSpeedLimit * 0.9
        roundedSpeedLimit = floorToNearest5(reducedSpeedLimit)


    # If medianSpeed (average speed of traffic) is less than 5 the new calculated speed limit
    # the medianSpeed will be floored to nearest 5 and will be declared the new speed limit.
    if medianSpeed < roundedSpeedLimit - 5:
        mSpeed = floorToNearest5(medianSpeed)
        if mSpeed < 60:
            mSpeed = 60
        return floorToNearest5(mSpeed)
    
    return roundedSpeedLimit
    

def floorToNearest5(numToRound):
    numToRoundDecimal = round((numToRound / 10) - int(numToRound / 10), 2)

    if numToRoundDecimal < 0.5:
        numToRoundDecimal = 0.0
        
    if numToRoundDecimal >= 0.5:
        numToRoundDecimal = 0.5

    return (int(numToRound / 10) + numToRoundDecimal) * 10


def calcFP(T, H):
    return (243.04 * (((T * 17.625) / (T + 243.04)) + math.log(H / 100))) / (17.625 - (((T * 17.625) / (T + 243.04)) + math.log(H / 100)))

def ClearScreen():
    display.fill(0)
    display.show()

def TestCode():
    display.fill(0)
    display.text("cntCNT",1,1,1) #The sign goes from top right to bottom left 
    display.show()
    #sleep(0.5)
    display.fill(0)
    display.text("CNTcnt",1,1,1) #The sign goes from top right to bottom left 
    display.show()
    #sleep(0.5)
    
    ShowSpeed(100,"K/H")
    sleep(5)
    FlickerSpeedUp(7)
    ShowSpeed(100,"K/H")
    sleep(5)
    FlickerSpeedDown(7)
    ShowSpeed(100,"K/H")
    

def ShowSlowDown():
    #fill (col)
    #pixel (x, y[, c])
    #hline (x, y, w, col)
    #vline (x, y, h, col)
    #line (x1, y1, x2, y2, col)
    #rect (x, y, w, h, col)
    #fill_rect (x, y, w, h, col)
    #text (string, x, y, col=1)
    #scroll (dx, dy)
    #blit (fbuf, x, y[, key])
    
    #S
    display.hline(27,1,3,1)
    display.hline(27,4,3,1)
    display.hline(27,7,3,1)
    display.vline(26,2,2,1)
    display.vline(30,5,2,1)
    display.pixel(26,6,1)
    display.pixel(30,2,1)
    
    #L
    display.vline(33,1,7,1)
    display.pixel(39,7,1)
    display.pixel(35,7,1)
    
    #O
    display.vline(38,1,7,1)
    display.vline(32,1,7,1)
    display.pixel(34,1,1)
    display.pixel(34,7,1)
    
    display.rect(9,1,3,7,1)
    
    #W
    display.vline(43,1,7,1)
    display.vline(45,2,6,1)
    display.vline(47,1,7,1)
    display.pixel(44,7,1)
    display.pixel(46,7,1)
    
    display.vline(14,1,7,1)
    display.vline(8,2,6,1) # For some reason this is the very right of the bottom middle display
    display.vline(18,1,7,1)
    display.pixel(15,7,1)
    display.pixel(17,7,1)
    
    #D
    display.hline(3,1,3,1)
    display.hline(3,7,3,1)
    display.vline(2,1,7,1)
    display.vline(6,2,5,1)
    
    #N
    display.vline(20,1,7,1)
    display.vline(23,1,7,1)
    display.pixel(21,3,1)
    display.pixel(22,4,1)
    display.show()
    
def FlickerSpeedDown(time):
    ClearScreen()
    for x in range(int(time)):
        ShowSlowDown()
        sleep_ms(500)
        display.fill(0)
        display.show()
        sleep_ms(500)
    
def ShowSpeedUp():
    #S
    display.hline(27,1,3,1)
    display.hline(27,4,3,1)
    display.hline(27,7,3,1)
    display.vline(26,2,2,1)
    display.vline(30,5,2,1)
    display.pixel(26,6,1)
    display.pixel(30,2,1)
    
    #P
    display.vline(24,1,7,1)
    display.pixel(33,1,1)
    display.pixel(33,4,1)
    display.vline(39,2,2,1)
    
    #E
    display.vline(36,1,7,1)
    display.hline(37,1,2,1)
    display.hline(37,4,2,1)
    display.hline(37,7,2,1)
    
    display.vline(32,1,7,1)
    display.hline(41,1,2,1)
    display.hline(41,4,2,1)
    display.hline(41,7,2,1)
    
    #D
    display.vline(44,1,7,1)
    display.hline(44,1,3,1)
    display.hline(44,7,3,1)
    display.vline(47,2,5,1)
    
    #U
    display.hline(9,7,2,1)
    display.vline(11,1,7,1)
    display.vline(0,1,7,1)
    
    #P
    display.vline(13,1,7,1)
    display.hline(14,1,2,1)
    display.hline(14,4,2,1)
    display.vline(8,2,2,1)
    
    display.show()
    
def FlickerSpeedUp(time):
    ClearScreen()
    for x in range(int(time)):
        ShowSpeedUp()
        sleep_ms(500)
        display.fill(0)
        display.show()
        sleep_ms(500)
    
def ShowSpeed(Speed, Units):
    if len(str(Speed)) == 3:
        Msg = str(Units) + str(Speed) 
    elif len(str(Speed)) == 2:
        Msg = str(Units) +  str(Speed) + " " 
    else:
        Msg = "  " + str(Units) + str(Speed)
    display.text(Msg,1,1,1)
    display.show()

def DebugWindow(Mode,LiveFreq,LiveSpeed,temp,hum):
    if Mode == 1:
        #for debugging
        oled.fill(0)
        oled.text("Debug Window", 0, 0)
        oled.text(f"LFreq : {str(LiveFreq)}", 0, 16)
        oled.text(f"LSpeed : {str(LiveSpeed)}", 0, 26)
        oled.text(f"Temp : {temp}", 0, 36)
        oled.text(f"Humid : {hum}", 0, 46)
        
        if adc.read_u16() < 30000:
            oled.text("Heavy Rain", 0, 56)
        elif adc.read_u16() < 45000:
            oled.text("Rain", 0, 56)
        else:
            oled.text("Clear Skies", 0, 56)
        oled.show()
    elif Mode == 0:
        print("---Debug Window---")
        print(f"LFreq : {str(LiveFreq)}",)
        print(f"LSpeed : {str(LiveSpeed)}")
        print(f"Temp : {temp}")
        print(f"Humid : {hum}")
        
        if adc.read_u16() < 30000:
            print("Heavy Rain")
        elif adc.read_u16() < 45000:
            print("Rain")
        else:
            print("Clear Skies")
        print("------------------")
        
    
    
############################################################################
#----------------------------------Inits-----------------------------------#
############################################################################
bme = bme280.BME280(i2c=i2c) # BME280 Initialization (SDA = GP6, SCL= GP7)
oled = SSD1306_I2C(128,64,si2c) # Oled Initialization (for debugging only)
display = max7219.Matrix8x8(spi,cs,6) # max7219 Initialization (CLK = GP2, DIN = GP3, CS = GP5 )

############################################################################
#---------------------------------Settings---------------------------------#
############################################################################
wifiName = "" # Wifi Name
wifiPassword = "" # Wifi Password
BaseSpeedLimit = 110 # Sets BaseSpeedLimit
display.brightness(15) # Sets Matrix Display Brightness to max level (1-15)

############################################################################
#----------------------------------Main------------------------------------#
############################################################################
#connect_to_wifi(wifiName, wifiPassword)
ClearScreen()
sleep_ms(1000) # Sleeps for 1 second
ShowSpeed(str(BaseSpeedLimit),"K/H")

SendCount = 0
SpeedCount = 0
Fq = 0
Speed = 0
AvgSpeed = 0
SpeedList = []
AverageSpeedList = []

while True:
    BaseSpeedLimit = 110
    SendCount += 1
    SpeedCount += 1

    temp = bme.values[0]
    hum = bme.values[2]
    raw_time = RTC().datetime()
    
    
    formatted_time = "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}.0Z".format(
    raw_time[0], raw_time[1], raw_time[2],
    raw_time[4], raw_time[5], raw_time[6]
    )

    #formatted_time = datetime(raw_time[0], raw_time[1], raw_time[2],raw_time[4], raw_time[5], raw_time[6])
    
    dfpoint = round(calcFP(float(temp[0:temp.index("C")]), float(hum[0:hum.index("%")])), 2)
    
    if ticks_diff(tmp := ticks_ms(), last_check) >= sampling_time:
        # Print calculated frequency in Hz - should show 1000 with default setup
        Fq = counter.read_and_reset() / (sampling_time / 1000)
        if Fq < 13:
            Fq = 0
        #oled.text(f"Freq : {str(counter.read_and_reset() / (sampling_time / 1000))}", 0, 30)
        last_check = tmp
        lSpeed = int(FreqToSpeed(Fq))
        
    if SpeedCount < 600: # Counts for 1 min
        if lSpeed > 0 and len(SpeedList) < 15:
            SpeedList.append(lSpeed)
        elif len(SpeedList) > 0 and lSpeed == 0:
            Speed = max(SpeedList)
            AverageSpeedList.append(Speed)
            SpeedList = []
            
            if len(AverageSpeedList) >= 3:
                print(f"Captured Speeds: {AverageSpeedList}")
                AvgSpeed = sum(AverageSpeedList) / len(AverageSpeedList)
                AverageSpeedList = []
            elif Speed > BaseSpeedLimit + 10:
                FlickerSpeedDown(7)
            elif Speed < BaseSpeedLimit - 10 and Speed != 0:
                FlickerSpeedUp(7)
            ShowSpeed(int(BaseSpeedLimit),"K/H")
            
    #DebugWindow(1,Fq,Speed,temp,hum) # Turn off to save power
    if SendCount >= 100: # 10 counts is 1 sec
        SendCount = 0
        if adc.read_u16() < 30000:
            RainStr = "Heavy Rain"
        elif adc.read_u16() < 45000:
            RainStr = "Rain"
        else:
            RainStr = "No Rain"
        print("---------------------------------------------")
        print("Current Speed Limit : " + str(BaseSpeedLimit))
        print(f"Captured Speeds: {AverageSpeedList}")
        print("AvgSpeed : " + str(AvgSpeed))
        print("Temperature: " + temp)
        print("Humidity: " + hum)
        print(f"Rain Status: {adc.read_u16()} -> {RainStr} ")
        print("Time:" + formatted_time)
        print("---------------------------------------------")
        #insertOne(temp, hum, AvgSpeed, RainStr, dfpoint, formatted_time)
        ClearScreen()
        if AvgSpeed > 0:
            BaseSpeedLimit = calculateNewSpeed(temp,hum,AvgSpeed, adc.read_u16())
            ShowSpeed(int(BaseSpeedLimit),"K/H")
        else:
            BaseSpeedLimit = calculateNewSpeed(temp,hum,BaseSpeedLimit, adc.read_u16())
            ShowSpeed(int(BaseSpeedLimit),"K/H")
        #deleteOne({"2024-03-15"}) # delete not working rn

