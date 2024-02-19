'''
Troy Husted
February 18, 2024
----------------
Description:
    This file tests the Linear Actuator
    Change the variable 'dc' to something between 0 -> 100.
    You will notice that the dc is inverse to the actual duty cycle that will
    be read on the oscilloscope.

    The hardware PWM signal will continue after running. Uncomment line 30 to stop the signal.
'''

import pigpio
import time
import sys
sys.path.append('/home/kwiat-test/Desktop/CUPSD/src/')
from HardPWM import HardwarePWM

# Test
pinNum = 12
freqHz = 1000
pin = HardwarePWM(pinNum, freqHz)
pin.pinpwm.set_mode(pinNum, pigpio.ALT0)

dc = 90 #inverse - a dc of 70 will correspond to an actual duty cycle of 30% on the oscilloscope
        # Note: a dc of 90 will mean the actuator is 90% extended

pin.pinpwm.hardware_PWM(pinNum, freqHz, dc*10000) #Pin, freq, duty cycle
# pin.end()

