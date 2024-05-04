"""
Troy Husted
March 5, 2024
----------------
Description:
    This file contains the function to (test) the magnetic brake torque to match the 
    required kapton tension - i.e. pull one value to check. This does not use any physical
    components.

    This code is divided into the several steps of what it takes to update the duty cycle
    of the PWM signal sent to the brakes.

    Step 1: We get the analog value from the follower arm. Using the ADC, we get a value
    between 0 and 1023

    Step 2: We find the approximate spool radius using the AV found in step 1. This is done
    by finding the amount of kapton on the spool using the provided ID and OD, and then finding
    essentially the fraction of Kapton remaining. 

    Step 3: We use the approximate spool radius to find the desired torque. We want the torque
    to match the desired tension as closely as possible. This is done by:
        - Convert the approximate spool radius found in Step 2 to m
        - Find the desired torque in NM
        - Convert the torque from NM to oz-in since that's what the curve units are

    Step 4: Find the two closest torques to the one found in Step 3 from the lower curve.

    Step 5: Interpolate from the two values found in Step 4 to get the closest duty cycle
    
    Example Use:
        python3 TensioningValueGrabSoftware.py
"""

import numpy as np


def TensionValueGrabSoftware(
    innerDiameterInches=3, outerDiameterInches=10.5, desiredTensionN=10
):
    """
    The maximum case (10.75 OD) is calibrated for the follower arm potentiometer, along with a nominal
    3in spool ID.

    @param desiredTension: Tension in newtons
    """
    ID = innerDiameterInches  # inches
    OD = outerDiameterInches  # inches
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

    # -------------------------------------------------------------
    # Step 1: Get analog value (av)
    # -------------------------------------------------------------
    av = 1023

    # -------------------------------------------------------------
    # Step 2: Get approximate spool radius
    # -------------------------------------------------------------
    kaptonOD = (OD - ID) / 2
    approxSpoolRadius = kaptonOD * (av / maxAnalog)
    print("Approximate spool radius: ", approxSpoolRadius)

    # -------------------------------------------------------------
    # Step 3: Use approximate spool radius and desired tension to find torque
    # -------------------------------------------------------------
    radiusMeters = approxSpoolRadius * 0.0254  # Convert inches to meters
    torque = desiredTensionN * radiusMeters  # Nm
    torqueOzIn = torque * 141.6119  # Oz*In
    print("Torque (Oz*In): ", torqueOzIn)

    # -------------------------------------------------------------
    # Step 4: Find values from dictionary lower curve values
    # -------------------------------------------------------------
    res_key_min, res_val_min = min(
        lowerCurve.items(), key=lambda x: abs(float(torqueOzIn) - float(x[1]))
    )  # Applies lambda function to each tuple
    tempLowerCurve = lowerCurve.copy()
    del tempLowerCurve[res_key_min]
    res_key_next, res_val_next = min(
        tempLowerCurve.items(), key=lambda x: abs(float(torqueOzIn) - float(x[1]))
    )  # Applies lambda function to each tuple
    print("Closest Value Key & Val: ", res_key_min, res_val_min)
    print("Next Closest Value Key & Val: ", res_key_next, res_val_next)

    # -------------------------------------------------------------
    # Step 5: Interpolate values from lower curves
    # -------------------------------------------------------------
    xCoords = [float(res_key_min), float(res_key_next)]
    yCoords = [float(res_val_min), float(res_val_next)]
    xCoords.sort()  # Sort ascending for interpolation
    yCoords.sort()
    finalDutyCycle = np.interp(float(torqueOzIn), yCoords, xCoords)
    print("Final duty cycle: ", round(finalDutyCycle, 2))


if __name__ == "__main__":
    TensionValueGrabSoftware(
        innerDiameterInches=3, outerDiameterInches=9.5, desiredTensionN=15
    )
