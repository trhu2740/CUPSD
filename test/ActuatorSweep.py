'''
Troy Husted
February 18, 2024
----------------
Description:
    This file tests the Linear Actuator range by sweeping through pulsewidths
        pulsewidth = 0 (off)
        pulsewidth = 1000 (safe anti-clockwise)
        pulsewidth = 1500 (center)
        pulsewidth = 2000 (safe clockwise)
'''

import pigpio
import sys
sys.path.append('/home/kwiat-test/Desktop/CUPSD/src/')
from Actuate import LinearActuate

pinNum = 18
pin = LinearActuate(pinNum)

try:
    while True:
        pin.pinpwm.set_servo_pulsewidth(pinNum, 1500) #Go to center

except KeyboardInterrupt:
    pin.end()
    print("Keyboard Interrupt")