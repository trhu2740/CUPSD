import sys

sys.path.append("/home/kwiat-test/Desktop/CUPSD/src/")
from AnalogRead import MCP3008_AnalogRead

adc = MCP3008_AnalogRead()

try:
    while True:
        print(adc.read(channel=7))  # if necessary perform several times
except KeyboardInterrupt:
    print("Interrupt")
