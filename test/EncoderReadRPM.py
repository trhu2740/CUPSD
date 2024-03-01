'''
Troy Husted
February 29, 2024
----------------
Description:
    This file contains code to read the encoder RPM.

        Channel 0: GPIO18, GPIO12
        Channel 1: GPIO13, GPIO19

    Example use:
        
'''

import RPi.GPIO as GPIO
import time

A_pin = 21
B_pin = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN)
GPIO.setup(B_pin, GPIO.IN)

# 1 rev = 3600

outcome = [0,-1,1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
last_AB = 0b00
counter = 0
last_time = time.time()  # Store the initial time

while True:
    A = GPIO.input(A_pin)
    B = GPIO.input(B_pin)
    current_AB = (A << 1) | B
    position  = (last_AB << 2) | current_AB
    counter += outcome[position]
    last_AB = current_AB
    
    # Calculate time difference
    current_time = time.time()
    time_diff = current_time - last_time
    last_time = current_time
    
    # Calculate RPM
    if time_diff != 0:  # To avoid division by zero
        rpm = (counter / 3600) / time_diff  # Counter is in revolutions, so divide by 3600 to get revolutions per second
        rpm *= 60  # Convert revolutions per second to revolutions per minute
        print("RPM:", rpm)
    else:
        print("RPM: N/A (No change in position)")