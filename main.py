from machine import Pin
import utime

# global params
buttonStartStop = Pin(11, Pin.IN, Pin.PULL_UP) # Start/Stop
buttonReverse = Pin(10, Pin.IN, Pin.PULL_UP) # Reverse
buttonReset = Pin(9, Pin.IN, Pin.PULL_UP) # Reset
buttonManual = Pin(8, Pin.IN, Pin.PULL_UP) # Manual
ledYellow = Pin(21, Pin.OUT) #Start/Stop LED
ledGreen = Pin(20, Pin.OUT) #Reverse LED
ledRed = Pin(22, Pin.OUT) #Reset LED
buzzer = Pin(26, Pin.OUT) #Buzzer
buttonPressed = 1 # PULL_UP so 1 is not pressed
onOff = 0 # by default don't start the counter
reverse = 0 # by default forword
nextNumberPlus = 1
nextNumberMinus = 9

# 7-segment display layout
#       A
#      ---
#  F |  G  | B
#      ---
#  E |     | C
#      ---
#       D

pins = [
    Pin(18, Pin.OUT),  # A
    Pin(19, Pin.OUT),  # B
    Pin(13, Pin.OUT),  # C
    Pin(14, Pin.OUT),  # D
    Pin(15, Pin.OUT),  # E
    Pin(17, Pin.OUT),  # F
    Pin(16, Pin.OUT),  # G
    Pin(12, Pin.OUT)   # DP 
]

# Common anode 7-segment display digit patterns
digits = [
    [0, 0, 0, 0, 0, 0, 1, 1], # 0
    [1, 0, 0, 1, 1, 1, 1, 1], # 1
    [0, 0, 1, 0, 0, 1, 0, 1], # 2 
    [0, 0, 0, 0, 1, 1, 0, 1], # 3
    [1, 0, 0, 1, 1, 0, 0, 1], # 4
    [0, 1, 0, 0, 1, 0, 0, 1], # 5
    [0, 1, 0, 0, 0, 0, 0, 1], # 6
    [0, 0, 0, 1, 1, 1, 1, 1], # 7
    [0, 0, 0, 0, 0, 0, 0, 1], # 8
    [0, 0, 0, 0, 1, 0, 0, 1], # 9
]

def clear():
    for i in pins:
        i.value(1)
        
def setZero():
    for j in range(len(pins)-1):
        pins[j].value(digits[0][j]) 
         
        
def waitAndDetectButtonPress(seconds):
    global onOff
    global reverse
    global nextNumberMinus
    global nextNumberPlus
    waitTime = seconds * 100
    while waitTime > 0:
        if buttonStartStop.value() == 0:
            ledYellow.toggle()
            if onOff == 0:
                print("Start")
                onOff = 1
            else:
                print("Stop")
                onOff = 0
            while buttonStartStop.value() == 0:
                utime.sleep(0.01)
            break
        elif buttonReverse.value() == 0:
            ledGreen.toggle()
            if reverse == 0:
                print("Backwards count")
                reverse = 1
            else:
                print("Fowrward count")
                reverse = 0
            while buttonReverse.value() == 0:
                utime.sleep(0.01)
            break
        elif buttonReset.value() == 0:
            ledRed.toggle()
            buzzer.value(1)
            print("Reset")
            setZero()
            if onOff == 1:
                ledYellow.toggle()
            onOff = 0
            if reverse == 1:
                ledGreen.toggle()
            reverse = 0
            nextNumberPlus = 1
            nextNumberMinus = 9
            while buttonReset.value() == 0:
                utime.sleep(0.6)
            ledRed.toggle()
            buzzer.value(0)
            break
        elif buttonManual.value() == 0:
            while buttonManual.value() == 0:
                manualCounterFunction()
            break
        else:
            utime.sleep(0.01)
            waitTime = waitTime - 1
            
def manualCounterFunction():
    global nextNumberPlus
    global nextNumberMinus
    buzzer.value(1)
    if reverse == 0:
        for j in range(len(pins)-1):
            pins[j].value(digits[nextNumberPlus][j]) 
        if nextNumberPlus == 9:
            nextNumberPlus = 0
        else:
            nextNumberMinus = nextNumberPlus - 1
            nextNumberPlus = nextNumberPlus + 1
    else:
        for j in range(len(pins)-1,-1,-1):
            pins[j].value(digits[nextNumberMinus][j]) 
        if nextNumberMinus == 0:
            nextNumberMinus = 9
        else:
            nextNumberPlus = nextNumberMinus + 1
            nextNumberMinus = nextNumberMinus - 1
            
    utime.sleep(0.1)
    buzzer.value(0)
    utime.sleep(0.4)
    

def countFunction():
    global nextNumberPlus
    global nextNumberMinus
    while reverse == 0:
        #print("Reverse 0")
        if onOff == 1: # On
            i = nextNumberPlus
            while i <= 9:
               #print(nextNumberPlus)
                if onOff == 1 and reverse == 0:
                    for j in range(len(pins)-1):
                        pins[j].value(digits[i][j])
                    if i == 9:
                        nextNumberPlus = 0
                    else: 
                        nextNumberPlus = i + 1
                        nextNumberMinus = i
                    i = nextNumberPlus
                    waitAndDetectButtonPress(1)
                else:
                    break
        else:
            waitAndDetectButtonPress(1)
        
def countBackwordsFunction():
    global nextNumberMinus
    global nextNumberPlus
    while reverse == 1:
        #print('Reverse 1')
        if onOff == 1: # On
            i = nextNumberMinus
            while i >= 0:
                #print(nextNumberMinus)
                if onOff == 1 and reverse == 1:
                    for j in range(len(pins)-1,-1,-1):
                        pins[j].value(digits[i][j])
                    if i == 0:
                        nextNumberMinus = 9
                    else: 
                        nextNumberMinus = i - 1
                        nextNumberPlus = i
                    i = nextNumberMinus
                    waitAndDetectButtonPress(1)
                else:
                    break
        else:
            waitAndDetectButtonPress(1)    

# Start run
setZero()

while True: 
    if reverse == 0:
        countFunction()
    else:
        countBackwordsFunction()


