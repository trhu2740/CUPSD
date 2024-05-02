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
    # -------------------------------------------------------------
    # Instantiate linear actuator class
    # -------------------------------------------------------------
    actuator = LinearActuate(GPIOPin)
    actuator.pinpwm.set_mode(GPIOPin, pigpio.ALT0)

    # -------------------------------------------------------------
    # Move the linear actuator to the desired position (command line input)
    # -------------------------------------------------------------
    actuator.changePosition(DC)


if __name__ == "__main__":
    # -------------------------------------------------------------
    # Try block tests to ensure a command line argument is given
    # -------------------------------------------------------------
    try:
        arg1 = sys.argv[  # If there's a command line argument (actuator position), set arg1 to it
            1
        ]
        arg2 = sys.argv[2]

    # -------------------------------------------------------------
    # For improper use, a usage statement is printed
    # -------------------------------------------------------------
    except IndexError:
        print(
            "Usage: " + os.path.basename(__file__) + "<pinNumber> <position>"
        )  # Print correct usage
        sys.exit(1)  # Terminate

    MoveLinearActuator(GPIOPin=arg1, DC=arg2)
