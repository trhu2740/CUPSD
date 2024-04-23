"""
Troy Husted
February 1, 2024
----------------
Description:
    This file contains the class for our analog read using an analog to digital converter (ADC)
    Example use:
    from ... import MCP3008_AnalogRead (include your relative path in ...)
"""

from spidev import SpiDev


class MCP3008_AnalogRead:
    """
    This class reads analog values from the analog to digital converter. Specify a bus or device
    when initializing if using anything other than zero.
    """

    def __init__(self, bus=0, device=0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000  # 1MHz

    def read(self, channel=0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def close(self):
        self.spi.close()
