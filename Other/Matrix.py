#!/bin/python3
import math
import os
import random
import re
import sys


matrix = [['T', '%'],
          ['h', '@'],
          ['#', 'x'],
          ['s', '#'],]
text = []
is_alnum = []
s = ''
r = len(matrix)
c = len(matrix[0])
l = []
for c0 in range(c):
    for r0 in range(r):
        text.append(matrix[r0][c0])
        is_alnum.append(matrix[r0][c0].isalnum())

print(text)
print(is_alnum)