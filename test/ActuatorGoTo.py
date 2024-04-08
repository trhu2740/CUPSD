"""
Troy Husted
February 18, 2024
----------------
Description:
    This file tests the Linear Actuator
    Change the variable 'dc' to something between 0 -> 100.
    You will notice that the dc is inverse to the actual duty cycle that will
    be read on the oscilloscope.

    The hardware PWM signal will continue after running. Uncomment line 30 to stop the signal.
"""

import pigpio
import time
import sys

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
from HardPWM import HardwarePWM

pinNum = 12  # Set the pin number on the raspberry pi for the linear actuator connection
freqHz = 1000  # Set the frequency in Hz for the hardware PWM frequency
pin = HardwarePWM(pinNum, freqHz)  # Instantiate HardwarePWM class to variable 'pin'
pin.pinpwm.set_mode(pinNum, pigpio.ALT0)

dc = 90  # inverse - a dc of 70 will correspond to an actual duty cycle of 30% on the oscilloscope
# Note: a dc of 90 will mean the actuator is 90% extended

pin.pinpwm.hardware_PWM(
    pinNum, freqHz, dc * 10000
)  # Pin, freq, duty cycle (duty cycle is out of 1 million)
