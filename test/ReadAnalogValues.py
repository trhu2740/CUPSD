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

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
from AnalogRead import MCP3008_AnalogRead

adc = MCP3008_AnalogRead()
chan = 7

try:
    while True:
        print(adc.read(channel=chan))  # if necessary perform several times
except KeyboardInterrupt:
    print("Interrupt")
