"""
Troy Husted
February 10, 2024
----------------
Description:
    This file tests the hardware PWM output by sweeping through duty cycles
    0 --> 100
    100 --> 0

    You will need to manually alter 'pinNum' and 'freqHz' accordingly. 

    Example Use:
        python3 HardPWMSweep.py
"""

import pigpio
import time
import sys

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
from HardPWM import HardwarePWM

# Test
pinNum = 18
freqHz = 50
pin = HardwarePWM(pinNum, freqHz)

try:
    while True:
        for dc in range(0, 100, 1):
            pin.pinpwm.hardware_PWM(pinNum, freqHz, dc * 10000)  # Pin, freq, duty cycle
            print(dc)
            time.sleep(0.1)
        for dc in range(100, 0, -1):
            pin.pinpwm.hardware_PWM(pinNum, freqHz, dc * 10000)  # Pin, freq, duty cycle
            print(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pin.end()
