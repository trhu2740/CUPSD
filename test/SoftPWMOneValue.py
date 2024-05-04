"""
Troy Husted
February 10, 2024
----------------
Description:
    This file is used to test the software PWM output on an oscilloscope.
    Change the variable 'dc' to something between 0 -> 100.

    Example use:
        python3 SoftPWMOneValue.py
"""

import RPi.GPIO as GPIO
import time
import sys

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
from SoftPWM import SoftwarePWM

pin40 = SoftwarePWM(40, 100)

dc = 10

try:
    while True:
        pin40.pinpwm.ChangeDutyCycle(dc)
except KeyboardInterrupt:
    pin40.end()
