'''
Troy Husted
February 18, 2024
----------------
Description:
    This file contains the class for moving the position of the T16-P Linear Actuator
    Example use:
    
'''
import pigpio

class LinearActuate:
    '''
    This class controls the movement of the linear actuator. With the accompanying LAC (Linear Actuator Controller)
    board, we can use the linear actuator as if it were a servo. 
        Note: We use the pigpio library for servo pulsewidth
            pulsewidth = 0 (off)
            pulsewidth = 1000 (safe anti-clockwise)
            pulsewidth = 1500 (center)
            pulsewidth = 2000 (safe clockwise)

            The selected pulsewidth will continue to be transmitted until changed by a subsequent call to 
            set_servo_pulsewidth.
    @param pin: Enter the (gpio) pin number on the raspberry pi
    '''

    def __init__(self, pin):
        self.pin = pin
        self.setup()

    def setup(self):
        self.pinpwm = pigpio.pi()
        self.pinpwm.set_servo_pulsewidth(self.pin, 0) #(pin, pulsewidth)

    def end(self):
        self.pinpwm.set_servo_pulsewidth(self.pin, 0)
        self.pinpwm.stop()