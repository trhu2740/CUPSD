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

from Actuate import LinearActuate


def MoveLinearActuator(GPIOPin, DC):
    actuator = LinearActuate(GPIOPin)  # Instantiate linear actuator class
    actuator.pinpwm.set_mode(GPIOPin, pigpio.ALT0)

    actuator.changePosition(
        DC
    )  # Move the linear actuator to the desired position (command line input)


if __name__ == "__main__":
    # Try block tests to ensure a command line argument is given
    try:
        arg1 = sys.argv[  # If there's a command line argument (actuator position), set arg1 to it
            1
        ]
        arg2 = sys.argv[2]

    except IndexError:  # For improper use, a usage statement is printed
        print(
            "Usage: " + os.path.basename(__file__) + "<pinNumber> <position>"
        )  # Print correct usage
        sys.exit(1)  # Terminate

    MoveLinearActuator(GPIOPin=arg1, DC=arg2)
