import RPi.GPIO as GPIO
import time


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

pin40 = SoftwarePWM(40, 50)

try:
    while True:
        for dc in range(0,100,1):
            pin40.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(0.1)
        for dc in range(100,0,-1):
                pin40.ChangeDutyCycle(dc)
                print(dc)
                time.sleep(0.1)
except KeyboardInterrupt:
      pin40.end()






GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
pinpwm = GPIO.PWM(40, 5) #pin #, freq in hz

def setup():
        pinpwm.start(0)

def loop():
        for dc in range(0,100,1):
                pinpwm.ChangeDutyCycle(dc)
                print(dc)
                time.sleep(0.1)
        for dc in range(100,0,-1):
                pinpwm.ChangeDutyCycle(dc)
                print(dc)
                time.sleep(0.1)
def end():
        pinpwm.stop()
        GPIO.cleanup()
