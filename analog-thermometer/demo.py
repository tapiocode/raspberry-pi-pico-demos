# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

import time
from analog_face import analog_face

thermometer_needle_face = analog_face([16, 17, 18, 19])

# The demo goes through the list of readings indefinitely
while True:
    print('Starting from zero (0)')
    for reading in [20, 60, 80, 120, 0]:
        print('Setting target', reading)
        thermometer_needle_face.set_target(reading)
        time.sleep(1)
