"""
Troy Husted
March 5, 2024
----------------
Description:
    This file contains the function to continuously update the magnetic brake torque to match the 
    required kapton tension.

    The one thing you may want to adjust is having to input a calibration OD every time you call 
    this function. Everything should be fairly straightforward.

    Example use:
        python3 Tensioning.py
"""

from AnalogRead import MCP3008_AnalogRead
from SoftPWM import SoftwarePWM
from gpiozero import MCP3008
import numpy as np


def Tension(
    innerDiameterInches,
    outerDiameterInches,
    desiredTensionN,
    magBrakePin,
    followerArmChannel,
):
    """
    OD_CALIBRATION: Must be the value that the potentiometer is calibrated to the max spool diameter.
    IF THE POTENTIOMETER IS NOT CALIBRATED SO THAT THE MAXIMUM VOLTAGE = MAX SPOOL DIAMETER:
        Adjust the maxAnalog accordingly

    @param innerDiameterInches: Inner diameter of Kapton spool in inches (nominal 3)
    @param outerDiameterInches: Outer diameter of Kapton spool in inches
    @param desiredTension: Tension in newtons
    @param magBrakePin: Magnetic Brake pin (NOT GPIO) (pin 13 or 15)
    """
    ID = innerDiameterInches  # inches
    OD_CALIBRATION = (
        outerDiameterInches  # inches (MUST be what the follower arm is calibrated to)
    )
    maxAnalog = 1023
    lowerCurve = {
        0: "7.00",
        5: "13.00",
        10: "23.00",
        15: "38.00",
        20: "48.00",
        25: "64.00",
        30: "112.00",
        35: "160.00",
        40: "192.00",
        45: "224.00",
        50: "272.00",
        55: "304.00",
        60: "336.00",
        65: "384.00",
        70: "416.00",
        75: "464.00",
        80: "496.00",
        85: "544.00",
        90: "592.00",
        95: "608.00",
        100: "656.000",
    }
    MagBrake = SoftwarePWM(magBrakePin, 50)
    followerArm = MCP3008_AnalogRead(0, 0, followerArmChannel)

    try:
        while True:
            # -------------------------------------------------------------
            # Step 1: Get analog value (av)
            # -------------------------------------------------------------
            av = followerArm.read()

            # -------------------------------------------------------------
            # Step 2: Get approximate spool radius
            # -------------------------------------------------------------
            kaptonOD = (OD_CALIBRATION - ID) / 2
            approxSpoolRadius = kaptonOD * (av / maxAnalog)
            print("Approximate spool radius: ", approxSpoolRadius)
            if approxSpoolRadius < 0.1:
                continue

            # -------------------------------------------------------------
            # Step 3: Use approximate spool radius and desired tension to find torque
            # -------------------------------------------------------------
            radiusMeters = approxSpoolRadius * 0.0254  # Convert inches to meters
            torque = desiredTensionN * radiusMeters  # Nm
            torqueOzIn = torque * 141.6119  # Oz*In
            # print("Torque (Oz*In): ", torqueOzIn)

            # -------------------------------------------------------------
            # Step 4: Find values from dictionary lower curve values
            # -------------------------------------------------------------
            res_key_min, res_val_min = min(
                lowerCurve.items(), key=lambda x: abs(float(torqueOzIn) - float(x[1]))
            )  # Applies lambda function to each tuple
            tempLowerCurve = lowerCurve.copy()
            del tempLowerCurve[res_key_min]
            res_key_next, res_val_next = min(
                tempLowerCurve.items(),
                key=lambda x: abs(float(torqueOzIn) - float(x[1])),
            )  # Applies lambda function to each tuple
            # print("Closest Value Key & Val: ", res_key_min, res_val_min)
            # print("Next Closest Value Key & Val: ", res_key_next, res_val_next)

            # -------------------------------------------------------------
            # Step 5: Interpolate values from lower curves
            # -------------------------------------------------------------
            xCoords = [float(res_key_min), float(res_key_next)]
            yCoords = [float(res_val_min), float(res_val_next)]
            xCoords.sort()  # Sort ascending for interpolation
            yCoords.sort()
            finalDutyCycle = np.interp(float(torqueOzIn), yCoords, xCoords)
            print("Final duty cycle: ", round(finalDutyCycle, 2))

            # -------------------------------------------------------------
            # Step 6: Update brake duty cycle
            # -------------------------------------------------------------
            MagBrake.pinpwm.ChangeDutyCycle(finalDutyCycle)

    except KeyboardInterrupt:
        print("interrupt")
        MagBrake.end()
        followerArm.close()


if __name__ == "__main__":
    Tension(
        innerDiameterInches=3,
        outerDiameterInches=9.5,
        desiredTensionN=15,
        magBrakePin=13,
        followerArmChannel=6,
    )
