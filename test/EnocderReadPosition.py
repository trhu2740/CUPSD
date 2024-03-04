'''
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
'''

import RPi.GPIO as GPIO

A_pin = 26
B_pin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN)
GPIO.setup(B_pin, GPIO.IN)

# 1 rev = 3600
outcome=[0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
#outcome = [0,-1,1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
last_AB = 0b00
counter = 0

while True:
    A = GPIO.input(A_pin)
    B = GPIO.input(B_pin)
    current_AB = (A << 1) | B
    position  = (last_AB << 2) | current_AB
    counter += outcome[position]
    last_AB = current_AB
    print(counter)
