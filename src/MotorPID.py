"""
Troy Husted
April 23, 2024
----------------
Description:
    

    Example use:
"""

import RPi.GPIO as GPIO
import pigpio
import time
import csv
from HardPWM import HardwarePWM
from MotorPIDClass import PIDController


def mainMotorLoop(
    EncoderAPin=2, EncoderBPin=3, setpointRPM=30, kp_in=0.6, ki_in=0.0, kd_in=0.0
):
    # Setup Motor. These contants don't need to change (unless you change PWM channel)
    MOTOR_GPIO_PIN = 13  # pin 12 is channel 0, pin 13 is channel 1 (motor)
    MOTOR_FREQUENCY_HZ = 20000
    MOTOR_STARTING_DC = 10

    # Initialize your motor and start it up to get the encoder reading values.
    current_DC = MOTOR_STARTING_DC
    motor = HardwarePWM(MOTOR_GPIO_PIN, MOTOR_FREQUENCY_HZ)  # PWM channel 1, 20kHz
    motor.pinpwm.set_mode(MOTOR_GPIO_PIN, pigpio.ALT0)
    motor.pinpwm.hardware_PWM(
        MOTOR_GPIO_PIN, MOTOR_FREQUENCY_HZ, MOTOR_STARTING_DC * 10000
    )  # Pin, freq, duty cycle

    # Setup Encoder. With the code shown in EncoderReadRPM, the encoder count is 7600.
    ENCODER_COUNT = 7600
    MOVEMENT_THRESHOLD = 5  # Adjust this value as needed
    ENCODER_TO_SHAFT_CONVERSION = (
        1.0186  # Comes from ratio of circumfrence of encoder to main tube
    )

    # These are typically pins 2 and 3 but can be adjusted if the PCB were to change
    A_pin = EncoderAPin  # GPIO Pin Number
    B_pin = EncoderBPin  # GPIO Pin Number

    # GPIO setup with A and B pins for encoder
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(A_pin, GPIO.IN)
    GPIO.setup(B_pin, GPIO.IN)

    # All possible outcomes for the encoder (see EncoderReadRPM.py)
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
    counter = 0  # Counter stores encoder counts
    prev_counter = 0
    last_time = time.time()  # Store the initial time

    # Set desired RPM
    setpoint_RPM = setpointRPM

    # PID constants
    kp = kp_in
    ki = ki_in
    kd = kd_in

    # Create controller
    pid = PIDController(setpoint_RPM, kp, ki, kd)

    current_rpm = 0  # Initial RPM
    rpm_values = []  # List to store RPM values

    try:
        while True:
            # Update Encoder (see EncoderReadRPM.py)
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
                MOTOR_GPIO_PIN, MOTOR_FREQUENCY_HZ, int(current_DC * 10000)
            )  # Update the PWM duty cycle. Inputs: (Pin, freq, duty cycle)

            rpm_values.append(current_rpm)  # Collect RPM value for csv output

    except KeyboardInterrupt:
        print("interrupt")
        motor.end()
        file_name = "rpm_values.csv"
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["RPM"])
            for rpm in rpm_values:
                writer.writerow([rpm])


if __name__ == "__main__":
    mainMotorLoop(setpointRPM=40, kp_in=0.6, ki_in=0.0, kd_in=0.0)
