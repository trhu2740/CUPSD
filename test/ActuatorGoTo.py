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

# -------------------------------------------------------------
# Set the pin number on the raspberry pi for the linear actuator connection
# -------------------------------------------------------------
pinNum = 12

# -------------------------------------------------------------
# Set the frequency in Hz for the hardware PWM frequency
# -------------------------------------------------------------
freqHz = 1000

# -------------------------------------------------------------
# Instantiate HardwarePWM class to variable 'pinNum'
# -------------------------------------------------------------
pin = HardwarePWM(pinNum, freqHz)
pin.pinpwm.set_mode(pinNum, pigpio.ALT0)

# -------------------------------------------------------------
# Example: a dc of 50 will mean the actuator is 50% extended
# -------------------------------------------------------------
dc = 50

pin.pinpwm.hardware_PWM(
    pinNum, freqHz, dc * 10000
)  # Pin, freq, duty cycle (duty cycle is out of 1 million)
