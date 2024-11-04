# John Luis Tayag
# Testing calculation algorithm for DSLS
import math
import random
baseSpeedLimit = 110

def FreqSpeed(SensorFreq, RecievedFreq , Temp):
    print(f"{RecievedFreq / 44}")
    
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


def Test(baseSpeed,Temp,Humid,medianSpeed, rainVal):
    print("---------------------------------------------------------")
    print(f"BaseSpeed Limit: {baseSpeed}")
    print(f"Temp: {Temp}")
    print(f"Humidity: {Humid}")
    print(f"Traffic Flow: {medianSpeed}")
    print(f"Rain Value: {rainVal}")
    print(f"Frost/dew Point: {round(calcFP(Temp, Humid), 2)}")
    if Humid == 100 and Temp < -5:
        print("Is at frost point")
    else:
        print("Is not at frost point")
    print()
    print(f"New Speed: {calculateNewSpeed(Temp, Humid, medianSpeed, rainVal)}")
    print("---------------------------------------------------------")


def main():
    # Tested dew point calculation based on data entries of 03/21/2024
    # print(round(calcFP(-7, 68), 2))
    # print(round(calcFP(-8, 74), 2))
    # print(round(calcFP(-8, 75), 2))
    # print(round(calcFP(-9, 79), 2))
    # print(round(calcFP(-10, 83), 2))
    # print(round(calcFP(-11, 84), 2))
    # print(round(calcFP(-11, 85), 2))
    # print(round(calcFP(-90, 100), 2))

    print()

def aveSpeed(Speed):
    return sum(Speed)/len(Speed)

main()


if __name__ == '__main__':
    while True:
        buffer = []
        #FreqSpeed(24000000, 158.42, 20)
        #baseSpeedLimit = random.randrange(60, 110)
        #Test(baseSpeedLimit, random.randrange(-10,23), 100, random.randrange(30,130))
        for x in range(100):
            buffer.append(random.randint(90, 120))

        print("At dew point")
        Test(baseSpeedLimit, -10, 100, 110, 65535)

        print(f"At negative temp but not 100% humididty")
        Test(baseSpeedLimit, -10, 50, 110, 65535)

        print("At 100 humidity but not at negative temp (-7 is the offset to account for difference between air and ground temp, air is colder than ground")
        Test(baseSpeedLimit, -6, 50, 110, 65535)

        print("At dew point but median speed is slower")
        Test(baseSpeedLimit, -10, 100, 70, 65535)

        print("Raining")
        Test(baseSpeedLimit, -10, 100, 110, 40000)

        print("Heavy rain")
        Test(baseSpeedLimit, -10, 100, 110, 35000)

        if input("Press enter to do another test") != "":
            break
