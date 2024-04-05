'''
Troy Husted
February 18, 2024
----------------
Description:
    This file contains the class for moving the position of the T16-P Linear Actuator.
    The use is almost exactly the same as the hardware PWM class since the linear actuator
    relies on the hardware PWM to extend & retract.

    Example use:
        from ... import LinearActuate (include your relative path in ...)
        actuator = LinearActuate(pinNum, freqHz)

'''
import pigpio

class LinearActuate:
    '''
    This class controls the movement of the linear actuator. With the accompanying LAC (Linear Actuator Controller)
    board, we use PWM to control the position. The LAC board requires a 3.3V, 1kHz PWM signal. A duty cycle of 0%
    corresponds to fully retracted, and a duty cycle of 100% corresponds to fully extended.

    @param pin: Enter the (gpio) pin number on the raspberry pi
    '''

    def __init__(self, pin):
        self.gpiopin = pin
        self.setup()

    def setup(self):
        self.pinpwm = pigpio.pi()
        self.pinpwm.set_mode(self.gpiopin, pigpio.OUTPUT)
        self.pinpwm.hardware_PWM(self.gpiopin, 0, 0) #Pin, freq, duty cycle

    def changePosition(self, dc):
        self.pinpwm.hardware_PWM(self.gpiopin, 1000, dc*10000) #Pin, freq, duty cycle

    def end(self):
        self.pinpwm.hardware_PWM(self.gpiopin, 0, 0) #Pin, freq, duty cycle
        self.pinpwm.stop()