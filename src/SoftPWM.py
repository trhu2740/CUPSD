'''
Troy Husted
February 8, 2024
----------------
Description:
    This file contains the class for our software PWM control using a raspberry pi
    Note: RPi.GPIO is capable of outputting software PWM on any GPIO pin. However,
        you may experience a 'jitter' or stutter in the signal as this signal is timed
        from the CPU clock. You will experience more stutter with higher frequencies. 
        Frequencies >5Khz are not reccommended for software PWM.

    Example use:
        from ... import SoftwarePWM (include your relative path in ...)
        pin40 = SoftwarePWM(40, 50)
        pin40.pinpwm.ChangeDutyCycle(dc)
'''

import RPi.GPIO as GPIO

class SoftwarePWM:
    '''
    This class controls software PWM
    @param pin: Enter the pin number on the raspberry pi
    @param freq: Enter the frequency in hz for the PWM signal
    '''
    def __init__(self, pin, freq):
        self.pin, self.freq = pin, freq
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pinpwm = GPIO.PWM(self.pin, self.freq)
        self.pinpwm.start(0) # Start with a duty cycle of 0

    def end(self):
           self.pinpwm.stop()
           GPIO.cleanup() # Will need to be an optional in the future
