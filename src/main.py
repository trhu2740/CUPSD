"""
Troy Husted
May 29, 2024
----------------
Description:
    This file contains the main usage to run the automated insulation wrapping machine.
    Changing the constants are super easy, and they are defined as per the functions themselves.
    Comments are provided above the constants to define what they are (reference only).

    Example use:
        python3 main.py
"""

import threading
from MotorPID import mainMotorLoop
from Tensioning import Tension
from HardPWM import HardwarePWM
from StopHardPWMAll import StopPWMHard


if __name__ == "__main__":
    try:
        # -------------------------------------------------------------
        # Initialize Motor Thread
        # -------------------------------------------------------------
        thread_1 = threading.Thread(
            target=mainMotorLoop,
            #     A, B, RPM, kp, ki,  kd
            args=(2, 3, 40, 0.6, 0.0, 0.0),
        )

        # -------------------------------------------------------------
        # Initialize Magnetic Brake Threads
        # -------------------------------------------------------------
        #                                                           ID, OD, N, MBP, AVC
        thread_2_PINK_BRAKE = threading.Thread(target=Tension, args=(3, 9.5, 15, 13, 7))
        thread_3_RED_BRAKE = threading.Thread(target=Tension, args=(3, 9.5, 15, 15, 6))

        # -------------------------------------------------------------
        # Start Threads
        # -------------------------------------------------------------
        thread_1.start()
        thread_2_PINK_BRAKE.start()
        thread_3_RED_BRAKE.start()

        # -------------------------------------------------------------
        # Join threads (good practice even though these are infinite loops)
        # -------------------------------------------------------------
        thread_1.join()
        thread_2_PINK_BRAKE.join()
        thread_3_RED_BRAKE.join()

    except KeyboardInterrupt:
        print("INTERRUPT")
        thread_1._stop()
        thread_2_PINK_BRAKE._stop()
        thread_3_RED_BRAKE._stop()

        # -------------------------------------------------------------
        # Stop PWM All Channels
        # -------------------------------------------------------------
        StopPWMHard()
