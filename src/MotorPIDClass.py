"""
Troy Husted
April 23, 2024
----------------
Description:
    (This will need future work - see MotorPID.py)

    This class controls the PID for the 300W drivetrain motor. It is very important to note that
    any PID for this machine is in discrete time, and thus it is not very possible for us to use
    a real PID loop / controller. Since this code is modular, you can easily replace this whole 
    class with new code if you would like (which I actually recommend). 
    Initializing this controller is super simple.

    This is designed to update the duty cycle that is sent to the motor. So, the primary input
    to this controller is the measured RPM from the quadrature encoder, and the primary output
    is the updated duty cycle. 

    I tried to keep this class very modular and simple to modify - so it shouldn't be too bad trying
    different things.

    Example use:
        # Initialize the controller
        pid = PIDController(setpoint_RPM, kp, ki, kd)

        # Update the PID
        current_DC = pid.update(current_rpm, current_DC)
"""


class PIDController:
    """
    (kp) Proportional Term: Directily proportional to the current error.
        a higher value will lead to higher overshoot and more oscillation
    (ki) Integral Term: Helps eliminate steady-state error, which can persist
        even after the system has stabalized. Ki is multiplied by the cumulative sum
        of all past errors, so it grows over time.
    (kd) Derivative Term: Helps predict future behavior of error based on currect rate of change
    """

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
        larger RPM values from dominating the update compared to lower RPM values.
        I am currently playing around with this so this is experimental.
        """
        normalized_error = error / self.setpoint_RPM
        normalized_derivative = derivative / self.setpoint_RPM

        output = (
            (self.kp * normalized_error)
            + (self.ki * self.integral)
            + (self.kd * normalized_derivative)
        )

        # -------------------------------------------------------------
        # Duty cycle is in the range of 0 to 100 (percentage)
        # -------------------------------------------------------------
        new_duty_cycle = current_duty_cycle + output

        # -------------------------------------------------------------
        # Ensure the duty cycle remains within the valid range (0 to 100)
        # -------------------------------------------------------------
        new_duty_cycle = max(0, min(100, new_duty_cycle))

        self.prev_error = error
        return new_duty_cycle
