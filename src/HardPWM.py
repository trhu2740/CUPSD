'''
Troy Husted
February 9, 2024
----------------
Description:
    This file contains the class for our hardware PWM control using a raspberry pi
    Note: There are only two channels for hardware PWM on the Raspberry Pi. Be aware that
        each channel is associated with two pins.

        Channel 0: GPIO18, GPIO12
        Channel 1: GPIO13, GPIO19

    Example use:
        from ... import SoftwarePWM (include your relative path in ...)
        pin = HardwarePWM(pinNum, freqHz)
        pin.pinpwm.hardware_PWM(pinNum, freqHz, dc*10000) #Pin, freq, duty cycle
        
'''
import pigpio
import time

class HardwarePWM:
    '''
    This class controls hardware PWM
    @param pin: Enter the (gpio) pin number on the raspberry pi
    @param freq: Enter the frequency in hz for the PWM signal
    '''

    def __init__(self, gpiopin, freq):
        self.gpiopin, self.freq = gpiopin, freq
        self.setup()

    def setup(self):
        self.pinpwm = pigpio.pi()
        self.pinpwm.set_mode(self.gpiopin, pigpio.OUTPUT)
        self.pinpwm.hardware_PWM(self.gpiopin, self.freq, 0) #Pin, freq, duty cycle

    def end(self):
        self.pinpwm.hardware_PWM(self.gpiopin, 0, 0*10000) #Pin, freq, duty cycle
        self.pinpwm.stop()