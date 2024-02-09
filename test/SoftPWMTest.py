'''
Troy Husted
February 8, 2024
----------------
Description:
    This file tests the PWM output by looping through duty cycles
    0 --> 100
    100 --> 0
'''

import RPi.GPIO as GPIO
import time
import sys
sys.path.append('/home/kwiat-test/Desktop/CUPSD/src/')
from SoftPWM import SoftwarePWM

pin40 = SoftwarePWM(40, 50)

try:
    while True:
        for dc in range(0,100,1):
            pin40.pinpwm.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(0.1)
        for dc in range(100,0,-1):
                pin40.pinpwm.ChangeDutyCycle(dc)
                print(dc)
                time.sleep(0.1)
except KeyboardInterrupt:
      pin40.end()