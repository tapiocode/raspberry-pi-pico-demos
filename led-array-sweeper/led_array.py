# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

from machine import Pin, PWM
import utime

# Amount of steps when changing PWM duty cycle from off to full
CYCLE_STEPS = 50
# Sleep between steps, in seconds
CYCLE_SLEEP = 0.002

MAX_DUTY = 255

class led_array:
    _pins: list[int]
    _led_sequence: list[int]
    _led_index = 0
    _leds = []

    def __init__(self, pins: list[int], led_sequence: None | str | list[int] = None):
        self._pins = pins
        if led_sequence != None:
            self.set_led_sequence(led_sequence)
        for gpio in pins:
            pwm = PWM(Pin(gpio))
            pwm.freq(1000)
            self._leds.append(pwm)

    # Immediately change currently executed sequence
    def set_led_sequence(self, led_sequence: str | list[int]) -> None:
        self._led_sequence = self._get_led_sequence(led_sequence) if type(led_sequence) is str else led_sequence
        self._led_index = 0

    # Start executing set sequence indefinitely
    def run(self):
        curr_duties = [0 for i in self._pins]
        curr_index = 0
        cycle_step = 0

        # The while-loop is fast enough to make brightness changes appear smooth to the eye
        while True:
            # When a new cycle (length of CYCLE_STEPS) starts, move on to the next in sequence
            if cycle_step == 0:
                curr_index = self._led_sequence[self._led_index]
                if self._led_index < len(self._led_sequence) - 1:
                    self._led_index += 1
                else:
                    self._led_index = 0

            # Linearly increase the brightness of the led at curr_index
            if curr_index > -1:
                next_duty = round(MAX_DUTY * (cycle_step/CYCLE_STEPS))
                curr_duties[curr_index] = max(next_duty, curr_duties[curr_index])

            # Go through all leds (except curr_index) and dim them just a tiny bit
            for i in range(len(self._pins)):
                duty = curr_duties[i]
                if curr_index != i and duty > 0:
                    duty -= 1
                self._leds[i].duty_u16(duty ** 2)
                curr_duties[i] = duty

            cycle_step = cycle_step + 1 if cycle_step < CYCLE_STEPS else 0
            utime.sleep(CYCLE_SLEEP)

    # Programmed sequence, available options to try:
    #   'linear'  - only one direction
    #   'sweeper' - sweep back and forth
    # Returns list of gpios[] index numbers to loop through. -1 means "skip".
    def _get_led_sequence(self, sequence: str) -> list[int]:

        # Simple sequence from 0 to (len - 1)
        if sequence == 'linear':
            return [i for i in range(len(self._pins))]

        # Sequence going up and down
        elif sequence == 'sweeper':
            seq = [-1, -1, -1] + self._get_led_sequence('linear') + [-1, -1, -1]
            seq.extend(range(len(self._pins) - 1, -1, -1))
            return seq

        raise ValueError('Invalid sequence "{}"'.format(sequence))
