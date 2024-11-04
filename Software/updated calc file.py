from machine import Pin, I2C, RTC
from time import sleep
import bme280
import urequests as requests
import network
import math
import random

# BASE SPEED LIMIT
baseSpeedLimit = 110


def connect_to_wifi(ssid, psk):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)
    
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect")
        sleep(10)
    if not wlan.isconnected():
        raise Exception("Wifi not available")
    print("Connected to Wifi")
    
    
def insertOne(temp, hum, avgSpeed, rainVal, DFPoint, time):
    try:
        url = "https://us-east-2.aws.data.mongodb-api.com/app/data-sxowy/endpoint/data/v1/action/insertOne"
        headers = { "api-key": "FU8kppU9XuZpgoRxGdAzTM1BftH9MgSGMGRdsToCSP9p2nVqpIka4HcfQHvbx27r" }
        
        data = {"temp": temp,
                "humidity": hum,
                "avgSpeed": avgSpeed,
                "rainVal": rainVal,
                "dFPoint": DFPoint,
                "time": time
                }
        
        payload = {
            "dataSource": "Cluster0",
            "database": "test",
            "collection": "weathers",
            "document": data,
        }
        
        response = requests.post(url=url, json=payload, headers=headers)
        
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        
        if response.status_code == 201:
            print("success")
        else:
            print("Error")
        
        response.close()
        
    except Exception as e:
        print(e)
    

def calculateNewSpeed(temperature, relativeHumidity, medianSpeed, rainVal):
    global baseSpeedLimit

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
        return floorToNearest5(medianSpeed)
    
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


connect_to_wifi("John", "dslswifi")
i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
while True: 
    bme = bme280.BME280(i2c=i2c)
    
    temp = bme.values[0]
    hum = bme.values[2]
    raw_time = RTC().datetime()
    dfpoint = round(calcFP(float(temp[0:temp.index("C")]), float(hum[0:hum.index("%")])), 2)
    formatted_time = "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}.0".format(
        raw_time[0], raw_time[1], raw_time[2],
        raw_time[4], raw_time[5], raw_time[6]
        )
    
    print("Temperature: " + temp)
    print("Humidity: " + hum)
    print("Time:" + formatted_time)
    print()
    
    insertOne(temp, hum, 60, 51358, dfpoint, formatted_time)
#     deleteOne({"2024-03-15"}) # delete not working rn
    
    sleep(10)
    
    
    
    
    
    
    
    
    
    
    
    
