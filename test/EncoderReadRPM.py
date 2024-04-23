"""
Troy Husted
March 4, 2024
----------------
Description:
    This file contains code to read the encoder RPM. This is calculated based on a change of encoder
    position over time. A constant - "MOVEMENT_THRESHOLD" is in place to control the precision of the 
    encoder RPM readout. This can be adjusted. You will only see different values when the encoder is moving.

    Any GPIO input pins can be used for the encoder.

    Example use:
    python3 EncoderReadRPM.py
        
"""

import RPi.GPIO as GPIO
import time

# Set a threshold for movement detection
ENCODER_COUNT = 7600
MOVEMENT_THRESHOLD = 5  # Adjust this value as needed
ENCODER_TO_SHAFT_CONVERSION = 1.0186  # Comes from ratio of circumfrence

A_pin = 2  # GPIO Pin Number
B_pin = 3  # GPIO Pin Number

GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN)
GPIO.setup(B_pin, GPIO.IN)

"""
Reading a quadrature encoder will have two waves: A & B
When determining encoder rotation and direction, we store 
the previous encoder values for A & B, as well as the current
encoder values for A & B. This gives 16 total possibilities.

Clearly, if the previous values match the current values, the encoder has not moved.
If, for example, the current A is different than the previous A, the encoder has moved.
    - this is also true for current B and previous B case
In an instance where both the current A and current B are different than the previous A
and B, we should not do anything (this is not expected behavior, as there should always be
a leading and trailing edge/channel)

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

outcome = [
    0,
    1,
    -1,
    0,
    -1,
    0,
    0,
    1,
    1,
    0,
    0,
    -1,
    0,
    -1,
    1,
    0,
]  # Result values from above

last_AB = 0b00
counter = 0
prev_counter = 0
last_time = time.time()  # Store the initial time

while True:
    A = GPIO.input(A_pin)  # Encoder channel A
    B = GPIO.input(B_pin)  # Encoder channel B

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

    # Calculate time difference - needed for RPM calculation below
    current_time = time.time()
    time_diff = current_time - last_time

    # Calculate RPM only when movement is significant
    counterDiff = counter - prev_counter
    if abs(counterDiff) > MOVEMENT_THRESHOLD and time_diff != 0:
        rpm = (counterDiff / ENCODER_COUNT) * (60 / time_diff)
        print("RPM: ", round(abs(rpm) * ENCODER_TO_SHAFT_CONVERSION, 2))
        prev_counter = counter
        last_time = current_time
    # else:
    #   print("RPM: N/A (No significant movement)")
