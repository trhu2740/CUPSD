import matplotlib.pyplot as plt

"""
    (kp) Proportional Term: Directily proportional to the current error.
        a higher value will lead to higher overshoot and more oscillation
    (ki) Integral Term: Helps eliminate steady-state error, which can persist
        even after the system has stabalized. Ki is multiplied by the cumulative sum
        of all past errors, so it grows over time.
    (kd) Derivative Term: Helps predict future behavior of error based on currect rate of change
"""

class PIDController:
    def __init__(self, setpoint, kp=1.0, ki=0.0, kd=0.0):
        self.setpoint = setpoint
        self.kp = kp # Proportional term
        self.ki = ki # Integral term
        self.kd = kd # Derivative term
        self.prev_error = 0
        self.integral = 0

    def update(self, measured_value):
        error = self.setpoint - measured_value
        self.integral += error
        derivative = error - self.prev_error

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        self.prev_error = error
        return output

if __name__ == "__main__":
    setpoint_rpm = 60

    # PID constants
    kp = 0.1
    ki = 0.01
    kd = 0.05

    # Create controller
    pid = PIDController(setpoint_rpm, kp, ki, kd)

    # Simulate motor RPM readings
    current_rpm = 0  # Initial RPM
    time_step = 1  # Time step

    rpm_values = []  # List to store RPM values

    for _ in range(200):  # Simulate for 10 iterations
        # Update PID controller with current RPM and get control signal
        control_signal = pid.update(current_rpm)

        # Simulate motor response to control signal (adjust RPM)
        current_rpm += control_signal
        print(control_signal)

        rpm_values.append(current_rpm)  # Collect RPM value

    # Plot RPM values
    plt.plot(range(len(rpm_values)), rpm_values, label='RPM')
    plt.xlabel('Timestep')
    plt.ylabel('RPM')
    plt.title('Motor RPM Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()