import threading
from MotorPID import mainMotorLoop
from Tensioning import Tension
from HardPWM import HardwarePWM

#                                    A,  B, RPM, kp, ki, kd
t1 = threading.Thread(target=mainMotorLoop, args=[[2, 3, 40, 0.6, 0.0, 0.0]])

#                               ID, OD, N, MBP, AVC
t2 = threading.Thread(target=Tension, args=[[3, 9.5, 15, 13, 0]])
t3 = threading.Thread(target=Tension, args=[[3, 9.5, 15, 15, 1]])

try:
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
except KeyboardInterrupt:
    print("INTERRUPT")

    # Stop PWM All Channels
    channel_0 = 12
    channel_1 = 13
    freqHz = 0

    pin = HardwarePWM(channel_0, freqHz)
    pin1 = HardwarePWM(channel_1, freqHz)

    pin.end()
    pin1.end()
