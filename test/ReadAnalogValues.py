"""
Troy Husted
May 29, 2024
----------------
Description:
    This file is used to read and print the analog values from the ADC.
    Change the channel by altering 'chan' between 0->7

    Example use:
        python3 ReadAnalogValues.py
"""

import sys
from gpiozero import MCP3008

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
adc = MCP3008(7)

try:
    while True:
        print(adc.value)  # if necessary perform several times
except KeyboardInterrupt:
    print("Interrupt")
