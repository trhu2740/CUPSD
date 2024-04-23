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
from HardPWM import HardwarePWM

# Set channel pins (GPIO)
channel_0 = 12
channel_1 = 13
freqHz = 0

# Stop PWM All Channels
pin = HardwarePWM(channel_0, freqHz)
pin1 = HardwarePWM(channel_1, freqHz)

pin.end()
pin1.end()
