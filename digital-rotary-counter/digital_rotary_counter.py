# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

from collections import namedtuple
from ssd1306 import SSD1306_I2C
from numbers import GLYPH_WIDTH, GLYPH_HEIGHT, nums
import framebuf
import time

Coords = namedtuple('Coords', ['x', 'y'])

# The wheel contains numbers from 0 to 9 twice to simplify rotation logic.
# Longest rotation is from 9 to 8 (rotates through 9, 0, 1, 2, ..., 7, 8).
def get_numbers_wheel() -> framebuf.FrameBuffer:
    return framebuf.FrameBuffer(
        nums[0] + nums[1] + nums[2] + nums[3] + nums[4] + \
        nums[5] + nums[6] + nums[7] + nums[8] + nums[9] + \
        nums[0] + nums[1] + nums[2] + nums[3] + nums[4] + \
        nums[5] + nums[6] + nums[7] + nums[8] + nums[9],
        GLYPH_WIDTH, GLYPH_HEIGHT * (len(nums) * 2), framebuf.MONO_HLSB)

class slot_wheel:

    is_finished = False

    _steps_to_target: int
    _slot_index: int
    _speed: int
    _decelerate_at: int
    _wheel: framebuf.FrameBuffer

    def __init__(self, slot_index, old_num, num) -> None:
        if old_num == num:
            self.is_finished = True
            return
        to_position = num if num > old_num else (10 + num)

        self._steps_to_target = GLYPH_HEIGHT * (to_position - old_num)
        self._slot_index = slot_index
        self._speed = 10
        self._decelerate_at = min(self._steps_to_target, 60)
        self._wheel = get_numbers_wheel()
        # Scroll to the initial position
        self._wheel.scroll(0, GLYPH_HEIGHT * old_num * -1)

    # Return glyph-sized cropped view of framebuffer of the current position of rotation
    def rotate(self) -> framebuf.FrameBuffer:
        # Gradually lower speed until it is at 1 (slowest change)
        if self._steps_to_target < self._decelerate_at:
            self._speed -= 1 if self._speed > 1 else 0

        if self._steps_to_target < self._speed:
            self._speed = self._steps_to_target
        self._steps_to_target -= self._speed
        self.is_finished = self._steps_to_target <= 0

        self._wheel.scroll(0, self._speed * -1)
        return framebuf.FrameBuffer(self._wheel, GLYPH_WIDTH, GLYPH_HEIGHT, framebuf.MONO_HLSB)

class digital_rotary_counter:

    _oled: SSD1306_I2C
    _wheels: int
    _slot_positions: list[Coords] = []
    _curr_nums: list[int] = []
    _slot_wheels: list[slot_wheel] = []

    def __init__(self, oled, pos_x: int, pos_y: int, wheels = 5):
        self._oled = oled
        self._wheels = wheels
        for i in range(self._wheels):
            self._slot_positions.append(Coords(pos_x + i * GLYPH_WIDTH, pos_y))
            self._curr_nums.append(0)
            self._slot_wheels.append(None)

    def reset(self) -> None:
        for x, y in self._slot_positions:
            fbuf = framebuf.FrameBuffer(nums[0], GLYPH_WIDTH, GLYPH_HEIGHT, framebuf.MONO_HLSB)
            self._oled.blit(fbuf, x, y)
        self._oled.show()

    def rotate_to(self, num: int) -> None:
        # Turn integer into zero-padded string, then into list
        # Eg. 512 -> ['0', '0', '5', '1', '2']
        target_nums = list(('{:0' + str(self._wheels) + 'd}').format(num))

        for index, target_num in enumerate(target_nums):
            old_num = self._curr_nums[index]
            self._curr_nums[index] = int(target_num)
            self._slot_wheels[index] = slot_wheel(index, old_num, self._curr_nums[index])

        while self._is_finished() == False:
            # Call blit() for all wheels before redrawing OLED with show()
            for rotator in self._slot_wheels:
                if rotator.is_finished == False:
                    self._oled.blit(rotator.rotate(), *(self._slot_positions[rotator._slot_index]))
            self._oled.show()

        time.sleep(0.2)

    def _is_finished(self) -> bool:
        is_finished = True
        for rotator in self._slot_wheels:
            is_finished = False if is_finished == False or rotator.is_finished == False else True
        return is_finished
