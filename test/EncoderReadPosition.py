"""
Troy Husted
February 9, 2024
----------------
Description:
    This file contains code to read the encoder position. A positive number indicates clockwise
    rotation, while a negative number indicates counterclockwise rotation. Note, this reads absolute
    position from the start position. You will only see different values when the encoder is moving.

    Any GPIO input pins can be used for the encoder.

    Example use:
        python3 EncoderReadPosition.py
"""

import RPi.GPIO as GPIO

# -------------------------------------------------------------
# These are typically pins 2 and 3 but can be adjusted if the PCB were to change
# -------------------------------------------------------------
A_pin = 2  # GPIO pin number
B_pin = 3  # GPIO pin number

# -------------------------------------------------------------
# GPIO setup with A and B pins for encoder
# -------------------------------------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN)
GPIO.setup(B_pin, GPIO.IN)

# 1 rev = 7200
"""
Reading a quadrature encoder will have two waves: A & B
When determining encoder rotation and direction, we store 
the previous encoder values for A & B, as well as the current
encoder values for A & B. This gives 16 total possibilities.

Clearly, if the previous values match the current values, the encoder has not moved.
If, for example, the current A is different than the previous A, the encoder has moved.
    - this is also true for current B and previous B case
In an instance where both the current A and current B are different than the previous A
and B, we should not do anything (this is not expected behavior)

Thus, the cases are outlined below with the result, or rather the expected behavior of
the encoder counter. The variable 'outcome' houses the result column.

Previous A | Previous B | Current A | Current B | Result
    0           0           0           0       |     0 (do nothing)
    0           0           0           1       |     1 (increase counter by 1)
    0           0           1           0       |    -1 (decrease counter by 1)
    0           0           1           1       |     0 (do nothing)
    0           1           0           0       |    -1 (decrease counter by 1)
    0           1           0           1       |     0 (do nothing)
    0           1           1           0       |     0 (do nothing)
    0           1           1           1       |     1 (increase counter by 1)
    1           0           0           0       |     1 (increase counter by 1)
    1           0           0           1       |     0 (do nothing)
    1           0           1           0       |     0 (do nothing)
    1           0           1           1       |    -1 (decrease counter by 1)
    1           1           0           0       |     0 (do nothing)
    1           1           0           1       |    -1 (decrease counter by 1)
    1           1           1           0       |     1 (increase counter by 1)
    1           1           1           1       |     0 (do nothing)
    
"""
# -------------------------------------------------------------
# All possible outcomes for the encoder
# -------------------------------------------------------------
outcome = [0, 1, -1, 0, -1, 0, 0, 1, 1, 0, 0, -1, 0, -1, 1, 0]

# -------------------------------------------------------------
# Preparing encoder counter
# -------------------------------------------------------------
last_AB = 0b00
counter = 0

while True:
    # -------------------------------------------------------------
    #  Update Encoder
    # -------------------------------------------------------------
    A = GPIO.input(A_pin)
    B = GPIO.input(B_pin)

    """
        The goal here is to create a 4 bit number. We get the previous state, shift over two bits,
        join onto the current state, and lookup result. In example:
        
        Example (binary numbers and bitwise operators):
            previous A = 0
            previous B = 1
            current A = 1
            current B = 1

            current_AB = (1 << 1) [result 10] | 1 --> 11
            position = (01 << 2) [result 0100] | 11 --> 111 (can be written as 0111)

            111 (binary) -> 7 (base 10)

            so, we lookup the outcome[7] = 1 (increase counter by 1)
    """

    current_AB = (A << 1) | B
    position = (last_AB << 2) | current_AB
    counter += outcome[position]
    last_AB = current_AB
    print(counter)
