import pigpio
import time
import sys
sys.path.append('/home/kwiat-test/Desktop/CUPSD/src/')
from Actuate import LinearActuate

pinNum = 12
actuator = LinearActuate(pinNum)
actuator.pinpwm.set_mode(pinNum, pigpio.ALT0)
actuator.changePosition(50)

