#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'plusMinus' function below.
#
# The function accepts INTEGER_ARRAY arr as parameter.
#

def plusMinus(arr):
    list_len = len(arr)
    pos = 0.0
    zeros = 0.0
    negs = 0.0
    for a in arr:
        if a>0:
            pos += 1
        elif a<0:
            negs += 1
        else:
            zeros += 1
    p = pos/list_len
    print(f'{p:.6f}')
    print(negs/list_len)
    print(zeros/list_len)

if __name__ == '__main__':

    plusMinus([1,2,-1,-1,0,0])
