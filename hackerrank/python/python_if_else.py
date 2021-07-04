#!/bin/python3

import math
import os
import random
import re
import sys


if __name__ == '__main__':
    num = int(input().strip())
    n = num % 2

    if n == 0 and (2 <= num <= 5):
        print('Not Weird')
    elif n == 0 and (6 <= num <= 20):
        print('Weird')
    elif n == 0 and (num > 20):
        print('Not Weird')
    elif n == 1:
        print('Weird')

