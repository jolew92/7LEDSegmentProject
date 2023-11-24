from machine import Pin
import utime

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

button = Pin(21, Pin.IN, Pin.PULL_UP)
buttonPressed = 1 # Not pressed at start
OnOff = 1
nextNumber = 0

def clear():
    for i in pins:
        i.value(0)
        
def waitAndDetectButtonPress(seconds):
    global OnOff
    waitTime = seconds * 100
    while waitTime > 0:
        if button.value() == 0:
            if OnOff == 0:
                OnOff = 1
            else:
                OnOff = 0
            utime.sleep(1)
            break
        else:
            utime.sleep(0.01)
            waitTime = waitTime - 1

clear()

while True:
    if OnOff == 1: # On
        i = nextNumber
        while i <= 9:
            if OnOff == 1:
                for j in range(len(pins)-1):
                    pins[j].value(digits[i][j])
                if i == 9:
                    nextNumber = 0
                else: 
                    nextNumber = i + 1
                i = nextNumber
                waitAndDetectButtonPress(1)
            else:
                break
    waitAndDetectButtonPress(1)