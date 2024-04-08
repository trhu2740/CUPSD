"""
Troy Husted
March 4, 2024
----------------
Description:
    This file tests the Linear Actuator using the LinearActuate class.
    Takes command line argument for position. Specify position as an integer
    between 1 -> 99.

    Example use:
        python3 ActuatorGoToClass.py 75
"""

import pigpio
import time
import sys
import os

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
from Actuate import LinearActuate

try:  # Try block tests to ensure a command line argument is given
    arg1 = sys.argv[
        1
    ]  # If there's a command line argument (actuator position), set arg1 to it

except IndexError:  # For improper use of this file, a usage statement is printed
    print("Usage: " + os.path.basename(__file__) + " <position>")  # Print correct usage
    sys.exit(1)  # Terminate

pinNum = 12  # Set the pin number on the raspberry pi for the linear actuator connection
actuator = LinearActuate(pinNum)  # Instantiate linear actuator class
actuator.pinpwm.set_mode(pinNum, pigpio.ALT0)

actuator.changePosition(
    int(arg1)
)  # Move the linear actuator to the desired position (command line input)
