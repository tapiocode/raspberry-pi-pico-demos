# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

import micropython
from led_array import led_array
from machine import Timer
micropython.alloc_emergency_exception_buf(100)

sequences = [
    'sweeper',
    'linear',
    [4, 5, 3, 6, 2, 7, 1, 8, 0, 9, -1, -1, -1, -1, -1, -1], # Burst out from center
    [-1, 3, 6, -1, 0, 2, 1, -1, 7, -1, 9, -1, 5, 4, -1, 8]  # Random
]
curr_sequence_index = 0

print('Starting')
def goto_next_sequence():
    global led_demo, sequences, curr_sequence_index

    # Loop through the array indices
    next = sequences[curr_sequence_index % len(sequences)]
    curr_sequence_index += 1

    print('Sequence: ', next)
    led_demo.set_led_sequence(next)

# Set up a periodic timer to trigger change
tim = Timer(
    period = 4000,
    mode = Timer.PERIODIC,
    callback = lambda t:goto_next_sequence()
)

led_demo = led_array([16, 17, 18, 19, 20, 21, 22, 26, 27, 28], 'sweeper')
# Script never exits after calling run()
led_demo.run()
