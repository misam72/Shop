#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'miniMaxSum' function below.
#
# The function accepts INTEGER_ARRAY arr as parameter.
#

def miniMaxSum(arr):
    arr.sort()
    min_sum = 0
    max_sum = 0
    for i in range(5):
        if i<4:
            min_sum += arr[i]
        if i>0:
            max_sum += arr[i]
    print(min_sum)
    print(max_sum)
    
    

if __name__ == '__main__':
    
    arr = [2,4,0,5,3]
    miniMaxSum(arr)
