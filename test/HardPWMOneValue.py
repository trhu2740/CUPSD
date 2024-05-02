"""
Troy Husted
March 7, 2024
----------------
Description:
    This file is used to test the hardware PWM output on an oscilloscope.
    Change the variable 'dc' to something between 0 -> 100.

    Example use:
    python3 HardPWMOneValue.py

"""

import pigpio
import time
import sys

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
from HardPWM import HardwarePWM

# -------------------------------------------------------------
# Set the pin number on the raspberry pi for the PWM
# -------------------------------------------------------------
pinNum = 13  # pin 12 is channel 0, pin 13 is channel 1 (motor)

# -------------------------------------------------------------
# Set the frequency in Hz for the hardware PWM frequency
# -------------------------------------------------------------
freqHz = 20000

# -------------------------------------------------------------
# Instantiate HardwarePWM class to variable 'pinNum'
# -------------------------------------------------------------
pin = HardwarePWM(pinNum, freqHz)
pin.pinpwm.set_mode(pinNum, pigpio.ALT0)

# -------------------------------------------------------------
# Example: a dc of 50 will mean 50% max voltage
# -------------------------------------------------------------
dc = 20

pin.pinpwm.hardware_PWM(pinNum, freqHz, dc * 10000)  # Pin, freq, duty cycle
# pin.end()
