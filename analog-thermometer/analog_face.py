# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

from stepper_motor import stepper_motor
import utime

class analog_face:

    _current_reading: int = 0
    _target_reading: int = 0
    _stepper_motor: stepper_motor

    def __init__(self, stepper_pins: list[int]):
        self._stepper_motor = stepper_motor(stepper_pins)

    def set_target(self, target: int):
        self._target_reading = target * 3
        while self._current_reading != self._target_reading:
            self._move_towards_target()

    def _move_towards_target(self):
        # Determine the speed of change, decelrating when nearing the target
        diff = min(30, abs(self._current_reading - self._target_reading))
        sleep = (30 - diff) * 2 + 1
        utime.sleep_ms(sleep)
        # Step size is always 1, the sign (+ or -) determines the direction of change
        step = 1 if self._current_reading < self._target_reading else -1
        self._current_reading += step
        self._stepper_motor.rotate(step)
