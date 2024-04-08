"""
Troy Husted
February 10, 2024
----------------
Description:
    This file is used to test the software PWM output on an oscilloscope.
    Change the variable 'dc' to something between 0 -> 100.
    You will notice that the dc is inverse to the actual duty cycle that will
    be read on the oscilloscope.

    Example use:
    python3 SoftPWMOneValue.py

"""

import RPi.GPIO as GPIO
import time
import sys

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
from SoftPWM import SoftwarePWM

pin40 = SoftwarePWM(40, 100)

dc = 10  # inverse : dc of 10 corresponds to an actual duty cycle of 90% on the scope

try:
    while True:
        pin40.pinpwm.ChangeDutyCycle(dc)
except KeyboardInterrupt:
    pin40.end()
