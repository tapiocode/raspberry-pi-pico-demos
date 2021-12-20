# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

from machine import Pin, PWM
import random
import time

MAX_DUTY = 255

GPIO_RED = 13
GPIO_GREEN = 14
GPIO_BLUE = 15

# Setting up the LEDs using PWM, and balancing the LED outputs to emit orangish glow
leds = [
    (PWM(Pin(GPIO_RED,   Pin.OUT)), 1.00),
    (PWM(Pin(GPIO_GREEN, Pin.OUT)), 0.30),
    (PWM(Pin(GPIO_BLUE,  Pin.OUT)), 0.03)
]
for led in leds:
    led[0].freq(1000)

def get_values_between(steps: int, curr: float, next: float) -> list[float]:
    intensities = []
    diff = next - curr
    for step in range(1, steps + 1):
        intensities.append(curr + diff * (step/steps))
    return intensities

# Returns a list of floats that plot a zig-zagging line used to produce a flickering effect
def get_random_intensities() -> list[float]:
    def get_random_intensity() -> float:
        return random.uniform(0.25, 1.0)

    intensities = []
    next_intensity = 0
    # Go through a range of intensity values, steadily increasing/decreasing
    # the value from current towards the next
    for i in range(23):
        curr_intensity = next_intensity if i > 0 else 1.0
        next_intensity = get_random_intensity()

        # Go through random number of equal size steps from current to the next
        steps = round(random.uniform(2, 29))
        intensities.extend(get_values_between(steps, curr_intensity, next_intensity))

    return intensities

def set_duties(intensity: float) -> None:
    for pin, power in leds:
        pin.duty_u16(round(intensity * MAX_DUTY * power) ** 2)
    time.sleep(0.02)

print('Starting')
set_duties(0)
time.sleep(1)

# Gently turn up the brightness from 0 to full
from_off_to_full = get_values_between(60, 0.0, 1.0)
for intensity in from_off_to_full:
    set_duties(intensity)

# Begin endless loop of randomly generated flicker
random_intensities = get_random_intensities()
while True:
    for intensity in random_intensities:
        set_duties(intensity)
