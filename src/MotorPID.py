import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import pigpio
import time
import sys

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
from HardPWM import HardwarePWM

"""
    (kp) Proportional Term: Directily proportional to the current error.
        a higher value will lead to higher overshoot and more oscillation
    (ki) Integral Term: Helps eliminate steady-state error, which can persist
        even after the system has stabalized. Ki is multiplied by the cumulative sum
        of all past errors, so it grows over time.
    (kd) Derivative Term: Helps predict future behavior of error based on currect rate of change
"""


class PIDController:
    def __init__(self, setpoint_RPM, kp=1.0, ki=0.0, kd=0.0):
        self.setpoint_RPM = setpoint_RPM
        self.kp = kp  # Proportional term
        self.ki = ki  # Integral term
        self.kd = kd  # Derivative term
        self.prev_error = 0
        self.integral = 0

    def update(self, measured_RPM, current_duty_cycle):
        error = self.setpoint_RPM - measured_RPM
        self.integral += error
        derivative = error - self.prev_error

        """
        Normalize error and derivative based on setpoint range. Prevents
        larger RPM values from dominating the update compared to lower RPM values
        """
        normalized_error = error / self.setpoint_RPM
        normalized_derivative = derivative / self.setpoint_RPM

        output = (
            (self.kp * normalized_error)
            + (self.ki * self.integral)
            + (self.kd * normalized_derivative)
        )

        # Duty cycle is in the range of 0 to 100 (percentage)
        new_duty_cycle = current_duty_cycle + output

        # Ensure the duty cycle remains within the valid range (0 to 100)
        new_duty_cycle = max(0, min(100, new_duty_cycle))

        self.prev_error = error
        return new_duty_cycle


if __name__ == "__main__":
    # Setup Motor
    MOTOR_GPIO_PIN = 13  # pin 12 is channel 0, pin 13 is channel 1 (motor)
    MOTOR_FREQUENCY_HZ = 20000
    MOTOR_STARTING_DC = 10
    current_DC = MOTOR_STARTING_DC
    motor = HardwarePWM(MOTOR_GPIO_PIN, MOTOR_FREQUENCY_HZ)  # PWM channel 1, 20kHz
    motor.pinpwm.set_mode(MOTOR_GPIO_PIN, pigpio.ALT0)
    motor.pinpwm.hardware_PWM(
        MOTOR_GPIO_PIN, MOTOR_FREQUENCY_HZ, MOTOR_STARTING_DC * 10000
    )  # Pin, freq, duty cycle

    # Setup Encoder
    ENCODER_COUNT = 7600
    MOVEMENT_THRESHOLD = 5  # Adjust this value as needed
    ENCODER_TO_SHAFT_CONVERSION = 3.4652  # Comes from ratio of circumfrence

    A_pin = 2  # GPIO Pin Number
    B_pin = 3  # GPIO Pin Number

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(A_pin, GPIO.IN)
    GPIO.setup(B_pin, GPIO.IN)
    outcome = [
        0,
        1,
        -1,
        0,
        -1,
        0,
        0,
        1,
        1,
        0,
        0,
        -1,
        0,
        -1,
        1,
        0,
    ]  # Result values from above

    last_AB = 0b00
    counter = 0
    prev_counter = 0
    last_time = time.time()  # Store the initial time

    # Set desired RPM
    setpoint_RPM_rpm = 30

    # PID constants
    kp = 0.05
    ki = 0.01
    kd = 0.1

    # Create controller
    pid = PIDController(setpoint_RPM_rpm, kp, ki, kd)

    # Simulate motor RPM readings
    current_rpm = 0  # Initial RPM
    time_step = 1  # Time step

    rpm_values = []  # List to store RPM values

    try:
        while True:
            # Update Encoder
            A = GPIO.input(A_pin)  # Encoder channel A
            B = GPIO.input(B_pin)  # Encoder channel B
            current_AB = (A << 1) | B
            position = (last_AB << 2) | current_AB
            counter += outcome[position]
            last_AB = current_AB

            # Calculate time difference - needed for RPM calculation below
            current_time = time.time()
            time_diff = current_time - last_time

            # Calculate RPM only when movement is significant
            counterDiff = counter - prev_counter
            if abs(counterDiff) > MOVEMENT_THRESHOLD and time_diff != 0:
                rpm = (counterDiff / ENCODER_COUNT) * (60 / time_diff)
                current_rpm = rpm
                print("RPM: ", round(abs(rpm) * ENCODER_TO_SHAFT_CONVERSION, 2))
                prev_counter = counter
                last_time = current_time
            else:
                # No significant movement
                continue

            # Update PID controller with current RPM and get new duty cycle
            current_DC = pid.update(current_rpm, current_DC)

            # Adjust Duty Cycle
            motor.pinpwm.hardware_PWM(
                MOTOR_GPIO_PIN, MOTOR_FREQUENCY_HZ, current_DC * 10000
            )  # Update the PWM duty cycle. Inputs: (Pin, freq, duty cycle)

            rpm_values.append(current_rpm)  # Collect RPM value

    except KeyboardInterrupt:
        print("interrupt")
        # Plot RPM values
        # plt.plot(range(len(rpm_values)), rpm_values, label="RPM")
        # plt.xlabel("Timestep")
        # plt.ylabel("RPM")
        # plt.title("Motor RPM Over Time")
        # plt.legend()
        # plt.grid(True)
        # plt.show()
