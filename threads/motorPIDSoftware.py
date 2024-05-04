"""
Troy Husted
May 29, 2024
----------------
Description:
    A separate software-only motor PID simulator for thread testing.

    Example use:
        python3 motorPIDSoftware.py
"""

import csv


class PIDController:
    def __init__(self, setpoint, kp=1.0, ki=0.0, kd=0.0):
        self.setpoint = setpoint
        self.kp = kp  # Proportional term
        self.ki = ki  # Integral term
        self.kd = kd  # Derivative term
        self.prev_error = 0
        self.integral = 0

    def update(self, measured_value):
        error = self.setpoint - measured_value
        self.integral += error
        derivative = error - self.prev_error

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        self.prev_error = error
        return output


def MotorSimulation(
    EncoderAPin=2, EncoderBPin=3, setpointRPM=30, kp_in=0.6, ki_in=0.0, kd_in=0.0
):
    while True:
        setpoint_rpm = setpointRPM

        # -------------------------------------------------------------
        # PID constants
        # -------------------------------------------------------------
        kp = kp_in
        ki = ki_in
        kd = kd_in

        # -------------------------------------------------------------
        # Create controller
        # -------------------------------------------------------------
        pid = PIDController(setpoint_rpm, kp, ki, kd)

        # -------------------------------------------------------------
        # Simulate motor RPM readings
        # -------------------------------------------------------------
        current_rpm = 0  # Initial RPM
        time_step = 1  # Time step

        # -------------------------------------------------------------
        #  rpm values array for logging
        # -------------------------------------------------------------
        rpm_values = []  # List to store RPM values

        # -------------------------------------------------------------
        #  Update PID controller with current RPM and get control signal
        # -------------------------------------------------------------
        control_signal = pid.update(current_rpm)

        # -------------------------------------------------------------
        #  Simulate motor response to control signal (adjust RPM)
        # -------------------------------------------------------------
        current_rpm += control_signal
        rpm_values.append(current_rpm)  # Collect RPM value

        file_name = "rpm_values.csv"
        with open(file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([current_rpm])


if __name__ == "__main__":
    MotorSimulation(
        EncoderAPin=2,
        EncoderBPin=3,
        setpointRPM=30,
        kp_in=0.6,
        ki_in=0.0,
        kd_in=0.0,
    )
