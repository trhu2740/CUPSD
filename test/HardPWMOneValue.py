'''
Troy Husted
March 7, 2024
----------------
Description:
    This file is used to test the hardware PWM output on an oscilloscope.
    Change the variable 'dc' to something between 0 -> 100.

    Example use:
    python3 HardPWMOneValue.py

'''


import pigpio
import time
import sys
sys.path.append('/home/kwiat-test/Desktop/CUPSD/src/')
from HardPWM import HardwarePWM

# Test
pinNum = 12
freqHz = 100
pin = HardwarePWM(pinNum, freqHz)
pin.pinpwm.set_mode(pinNum, pigpio.ALT0)

dc = 90 #inverse - a dc of 70 will correspond to an actual duty cycle of 30% on the oscilloscope
        # Note: a dc of 90 will mean the actuator is 90% extended

pin.pinpwm.hardware_PWM(pinNum, freqHz, dc*10000) #Pin, freq, duty cycle
# pin.end()







