'''
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
        
'''

import RPi.GPIO as GPIO
import time

A_pin = 26
B_pin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN)
GPIO.setup(B_pin, GPIO.IN)

# 1 rev = 7200
outcome = [0, 1, -1, 0, -1, 0, 0, 1, 1, 0, 0, -1, 0, -1, 1, 0]

last_AB = 0b00
counter = 0
prev_counter = 0
last_time = time.time()  # Store the initial time

# Set a threshold for movement detection
MOVEMENT_THRESHOLD = 5  # Adjust this value as needed

while True:
    A = GPIO.input(A_pin)
    B = GPIO.input(B_pin)
    current_AB = (A << 1) | B
    position = (last_AB << 2) | current_AB
    counter += outcome[position]
    last_AB = current_AB

    # Calculate time difference
    current_time = time.time()
    time_diff = current_time - last_time

    # Calculate RPM only when movement is significant
    counterDiff = counter - prev_counter
    if abs(counterDiff) > MOVEMENT_THRESHOLD and time_diff != 0:
        rpm = (counterDiff / 7200) * (60 / time_diff)
        print("RPM:", abs(rpm))
        prev_counter = counter
        last_time = current_time
    #else:
     #   print("RPM: N/A (No significant movement)")