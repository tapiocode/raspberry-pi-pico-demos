# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

# SBC-OLED01, joy-it.net
# SCL = GP17
# SDA = GP16
# Display Image & text on I2C driven ssd1306 OLED display

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from digital_rotary_counter import digital_rotary_counter
import time

PIN_SCL = 17
PIN_SDA = 16
OLED_WIDTH = 128
OLED_HEIGHT = 64

i2c = I2C(0, scl = Pin(PIN_SCL), sda = Pin(PIN_SDA), freq = 200000)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# Flourish screen with frames and text
oled.fill(0)
oled.text('SSD1306 Demo', 16, 7)
oled.rect(2, 0, 124, 64, 1)
oled.rect(0, 2, 128, 60, 1)

print('Starting demo')
counter = digital_rotary_counter(oled, pos_x = 14, pos_y = 21, wheels = 5)
counter.reset()

# Start going through sequence of numbers indefinitely
while True:
    time.sleep(0.5)
    counter.rotate_to(11111)
    counter.rotate_to(1010)
    counter.rotate_to(43210)
    time.sleep(0.5)
    for i in range(99990, 100000, 1):
        counter.rotate_to(i)
    counter.rotate_to(0)
    time.sleep(1)
