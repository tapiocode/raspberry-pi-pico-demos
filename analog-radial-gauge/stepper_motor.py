# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

# 28BYJ-48 stepper motor with ULN2003 driver board
from machine import Pin
import utime

HALF_STEP = [
    [True,   False,  False,  False],
    [True,   True,   False,  False],
    [False,  True,   False,  False],
    [False,  True,   True,   False],
    [False,  False,  True,   False],
    [False,  False,  True,   True ],
    [False,  False,  False,  True ],
    [True,   False,  False,  True ]
]

class stepper_motor:
    _pin_range = range(4)
    _pins = []

    def __init__(self, pin_numbers: list[int]):
        for pin_number in pin_numbers:
            pin = Pin(pin_number, Pin.OUT)
            pin.low()
            self._pins.append(pin)

    def rotate(self, clockwise: int) -> None:
        for vals in HALF_STEP[::clockwise]:
            for idx, val in enumerate(vals):
                self._pins[idx].value(val)
            utime.sleep_ms(1)
