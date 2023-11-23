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
def clear():
    for i in pins:
        i.value(0)
clear()
while True:
    for i in range(len(digits)):
        for j in range(len(pins)-1):
            pins[j].value(digits[i][j])
        utime.sleep(1)