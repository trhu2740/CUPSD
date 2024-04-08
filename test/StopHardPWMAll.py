"""
Troy Husted
February 8, 2024
----------------
Description:
    This file stops hardware PWM on all channels (channel 0 & channel 1)

    Example use:
    python3 StopHardPWMAll.py
"""

import pigpio
import time
import sys

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
from HardPWM import HardwarePWM

# Stop PWM All Channels
pinNum = 12
pinNum1 = 13
freqHz = 0
pin = HardwarePWM(pinNum, freqHz)
pin1 = HardwarePWM(pinNum1, freqHz)

pin.end()
pin1.end()
