#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'timeConversion' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def timeConversion(s):
    ho = s[0:2]
    mi = s[3:5]
    se = s[6:8]
    is_am = True if s[8:] == 'AM' else False
    if is_am:
        if ho == '12':
            ho = '00'
    else:
        if ho != '12':
            ho = int(ho)
            ho += 12
        ho = str(ho)
    print(f'{ho}:{mi}:{se}')

if __name__ == '__main__':

    s = '12:05:39PM'

    timeConversion(s)
