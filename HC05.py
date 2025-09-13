"""
HC_05.py
TrailMapInterface V1.0
"""

import serial
# import time

bluetooth = serial.Serial("/dev/rfcomm2", 9600) # send serial value

"""
States for Easy Trails
"""
chaseItState = ''
crackerjackState = ''
learningZoneState = ''
lowerBoulevardState = ''
lowerEastMeadowState = ''
lowerThruwayState = ''
plazaState = ''
proutysPastState = ''
runAround1State = ''
runAround2State = ''
runAround3State = ''
runAround4State = ''
schoolSlopeState = ''
woodsRunState = ''

"""
Getters for Easy Trails
"""
def getChaseItState():
    return chaseItState
def getCrackerjackState():
    return crackerjackState
def getLearningZoneState():
    return learningZoneState
def getLowerBoulevardState():
    return lowerBoulevardState
def getLowerEastMeadowState():
    return lowerEastMeadowState
def getLowerThruwayState():
    return lowerThruwayState
def getPlazaState():
    return plazaState
def getProutysPastState():
    return proutysPastState
def getRunAround1State():
    return runAround1State
def getRunAround2State():
    return runAround2State
def getRunAround3State():
    return runAround3State
def getRunAround4State():
    return runAround4State
def getSchoolSlopeState():
    return schoolSlopeState
def getWoodsRunState():
    return woodsRunState

# sets lightState and doorState variables to their approriate values, depending on the current state of the light and door servos
def loadCurrentStates():
    with open('states.txt') as file:
        lines = []
        for line in file:
            lines.append(line)

        # create global variables to use for titles in file
        global chaseItState, crackerjackState, learningZoneState, lowerBoulevardState, lowerEastMeadowState
        global lowerThruwayState, plazaState, proutysPastState, runAround1State, runAround2State
        global runAround3State, runAround4State, schoolSlopeState, woodsRunState
        chaseItState = lines[0]
        crackerjackState = lines[1]
        learningZoneState = lines[2]
        lowerBoulevardState = lines[3]
        lowerEastMeadowState = lines[4]
        lowerThruwayState = lines[5]
        plazaState = lines[6]
        proutysPastState = lines[7]
        runAround1State = lines[8]
        runAround2State = lines[9]
        runAround3State = lines[10]
        runAround4State = lines[11]
        schoolSlopeState = lines[12]
        woodsRunState = lines[13]


        print("CHASE IT STATE: " + chaseItState)
        print("CRACKERJACK STATE: " + crackerjackState)
        print("LEARNING ZONE STATE: " + learningZoneState)
        print("LOWER BOULEVARD STATE: " + lowerBoulevardState)
        print("LOWER EAST MEADOW STATE: " + lowerEastMeadowState)
        print("LOWER THRUWAY STATE: " + lowerThruwayState)
        print("PROUTYS PAST STATE: " + proutysPastState)
        print("RUN AROUND 1 STATE: " + runAround1State)
        print("RUN AROUND 2 STATE: " + runAround2State)
        print("RUN AROUND 3 STATE: " + runAround3State)
        print("RUN AROUND 4 STATE: " + runAround4State)
        print("SCHOOL SLOPE STATE: " + schoolSlopeState)
        print("WOODS RUN STATE: " + woodsRunState)


loadCurrentStates()

# updates state file to hold current values of lightState and doorState variables
def updateStates():
    with open('states.txt', 'w') as file:
        file.write(chaseItState)
        file.write(crackerjackState)
        file.write(learningZoneState)
        file.write(lowerBoulevardState)
        file.write(lowerEastMeadowState)
        file.write(lowerThruwayState)
        file.write(proutysPastState)
        file.write(runAround1State)
        file.write(runAround2State)
        file.write(runAround3State)
        file.write(runAround4State)
        file.write(schoolSlopeState)
        file.write(woodsRunState)

    print("UPDATED CHASE IT STATE: " + chaseItState)
    print("UPDATED CRACKERJACK STATE: " + crackerjackState)
    print("UPDATED LEARNING ZONE STATE: " + learningZoneState)
    print("UPDATED LOWER BOULEVARD STATE: " + lowerBoulevardState)
    print("UPDATED LOWER EAST MEADOW STATE: " + lowerEastMeadowState)
    print("UPDATED LOWER THRUWAY STATE: " + lowerThruwayState)
    print("UPDATED PROUTYS PAST STATE: " + proutysPastState)
    print("UPDATED RUN AROUND 1 STATE: " + runAround1State)
    print("UPDATED RUN AROUND 2 STATE: " + runAround2State)
    print("UPDATED RUN AROUND 3 STATE: " + runAround3State)
    print("UPDATED RUN AROUND 4 STATE: " + runAround4State)
    print("UPDATED SCHOOL SLOPE STATE: " + schoolSlopeState)
    print("UPDATED WOODS RUN STATE: " + woodsRunState)

# Sends a serial code 'a' to Arduino
def send_bluetooth_data(a):
    string = 'X{0}'.format(a) # format of our data
    print('Serial code:' + string)
    bluetooth.write(string.encode("utf-8"))

    updateStates()

def chaseIt_open():
    global chaseItState
    if (chaseItState == 'delayed\n' or chaseItState == 'closed\n'):
        chaseItState = 'open\n'
        send_bluetooth_data(100)
def chaseIt_delayed():
    global chaseItState
    if (chaseItState == 'open\n' or chaseItState == 'closed\n'):
        chaseItState = 'delayed\n'
        send_bluetooth_data(200)
def chaseIt_closed():
    global chaseItState
    if (chaseItState == 'open\n' or chaseItState == 'delayed\n'):
        chaseItState = 'closed\n'
        send_bluetooth_data(300)

# def light_on():
#     global lightState
#     if lightState == 'off\n':
#         lightState = 'on\n'
#         send_bluetooth_data(300)
#
# def light_off():
#     global lightState
#     if lightState == 'on\n':
#         lightState = 'off\n'
#         send_bluetooth_data(400)
#
# def lock_door():
#     global doorState
#     if doorState == 'unlocked\n':
#         doorState = 'locked\n'
#         send_bluetooth_data(500)
#
# def unlock_door():
#     global doorState
#     if doorState == 'locked\n':
#         doorState = 'unlocked\n'
#         send_bluetooth_data(600)

# main loop for testing only
if __name__ == "__main__":
    while True:
        a = input("enter: -") # input value to be received by arduino bluetooth
        ''' this is where we can determine what pins we want on to control each
        component independently '''

        send_bluetooth_data(a)