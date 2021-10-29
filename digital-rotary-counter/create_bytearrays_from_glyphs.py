#!/usr/bin/env python3

# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

# This is a helper script written in python3, so it's not for the Pico.
#
# Reads the PBM-files from numbers/-directory and prints out python code for
# the demo. If you edit the number files you can update numbers.py by running:
#
#   ./create_bytearrays_from_glyphs.py > numbers.py
#
print('')
print('# Autogenerated content, see create_bytearrays_from_glyphs.py')
print('')
for i in range(10):
    with open(f'numbers/{i}.pbm', 'rb') as fd:
        fd.readline() # 'P4'
        fd.readline() # Comment line
        dims = [int(d) for d in fd.readline().strip().split()]
        data = fd.readline()
        if i == 0:
            print(f'GLYPH_WIDTH = {dims[0]}')
            print(f'GLYPH_HEIGHT = {dims[1]}')
            print('nums = []')
        print(f'nums.append(bytearray({data}))')