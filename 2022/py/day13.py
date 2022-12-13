from typing import *
from timer import Timer
import copy
import re
from dataclasses import dataclass, field
import math
from collections import deque

import itertools
import functools


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            pairs = [eval(line.strip()) 
                     for line in f.readlines() 
                     if line.strip() != ""]

    def compare(left, right):
        if isinstance(left, int) or isinstance(right, int):
            if isinstance(left, int) and isinstance(right, int):
                return left - right
            elif isinstance(left, int):
                return compare([left], right)
            else:
                return compare(left, [right])
        else: # two lists
            if len(left) == 0 or len(right) == 0:
                return len(left) - len(right)
            else:
                result = compare(left[0], right[0])
                if result == 0:
                    return compare(left[1:], right[1:])
                else:
                    return result

    with Timer("part 1"):
        total = 0
        for i in range(0, len(pairs), 2):
            if compare(pairs[i], pairs[i+1]) < 0:
                total += i//2 + 1

        print("part 1:", total)

    with Timer("part 2"):
        pairs.extend([[[2]], [[6]]])
        pairs = sorted(pairs, key=functools.cmp_to_key(compare))
        x1 = pairs.index([[2]]) + 1
        x2 = pairs.index([[6]]) + 1
        print("part 2:", x1*x2)


if __name__ == '__main__':
    main()
