'''
Troy Husted
February 9, 2024
----------------
Description:
    This file contains the class for our hardware PWM control using a raspberry pi
    Example use:
        from ... import SoftwarePWM (include your relative path in ...)
        
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
        self.pinpwm.set_PWM_frequency(self.gpiopin, self.freq)
        self.pinpwm.set_PWM_dutycycle(self.gpiopin, 0)

    def end(self):
        self.pinpwm.set_PWM_frequency(self.gpiopin, 0)
        self.pinpwm.stop()

# Test
pin12 = HardwarePWM(12, 50)
pin12.pinpwm.set_PWM_dutycycle(12, 25)

try:
    while True:
        for dc in range(0,100,1):
            pin12.pinpwm.set_PWM_dutycycle(12, dc)
            print(dc)
            time.sleep(0.1)
        for dc in range(100,0,-1):
            pin12.pinpwm.set_PWM_dutycycle(12, dc)
            print(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
      pin12.end()