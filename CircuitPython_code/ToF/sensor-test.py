# REFERENCE:
# https://docs.circuitpython.org/projects/tca9548a/en/latest/examples.html
# https://github.com/adafruit/Adafruit_CircuitPython_VL6180X/blob/main/examples/vl6180x_simpletest.py
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-i2c


# Demo of reading the range and lux from the VL6180x distance sensor and
# printing it every second.

import time
import board
import busio
import adafruit_vl6180x
import adafruit_tca9548a

print("===============")
print("ToF Sensor Test")
print("===============\n")

# BEGIN MUX SETUP
# This example shows using TCA9548A to perform a simple scan for connected devices

# Create I2C bus as normal
i2c = busio.I2C(board.D16,board.D17)

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

# for channel in range(8):
#     if tca[channel].try_lock():
#         print("Channel {}:".format(channel), end="")
#         addresses = tca[channel].scan()
#         print([hex(address) for address in addresses if address != 0x70])
#         tca[channel].unlock()


# CONTINUE SENSOR SETUP
# Create sensor instance.
sensor = None
sensor[0] = adafruit_vl6180x.VL6180X(tca[0])
sensor[1] = adafruit_vl6180x.VL6180X(tca[1])
sensor[2] = adafruit_vl6180x.VL6180X(tca[2])
sensor[3] = adafruit_vl6180x.VL6180X(tca[3])
# You can add an offset to distance measurements here (e.g. calibration)
# Swapping for the following would add a +10 millimeter offset to measurements:
# sensor = adafruit_vl6180x.VL6180X(i2c, offset=10)

# Main loop prints the range and lux every second:
while True:
    # Read the range in millimeters and print it.
    for i in range(4):
        range_mm = i.range
        print("S{1}: {0}mm".format(range_mm,i))
        # Read the light, note this requires specifying a gain value:
        adafruit_vl6180x.ALS_GAIN_1
        # - adafruit_vl6180x.ALS_GAIN_1 = 1x
        # - adafruit_vl6180x.ALS_GAIN_1_25 = 1.25x
        # - adafruit_vl6180x.ALS_GAIN_1_67 = 1.67x
        # - adafruit_vl6180x.ALS_GAIN_2_5 = 2.5x
        # - adafruit_vl6180x.ALS_GAIN_5 = 5x
        # - adafruit_vl6180x.ALS_GAIN_10 = 10x
        # - adafruit_vl6180x.ALS_GAIN_20 = 20x
        # - adafruit_vl6180x.ALS_GAIN_40 = 40x
        light_lux = i.read_lux(adafruit_vl6180x.ALS_GAIN_1)
        print("Light (1x gain): {0}lux".format(light_lux))
        # Delay for a second.
        time.sleep(1.0)
