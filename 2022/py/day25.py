from typing import *
from timer import Timer
import copy
import heapq
import re
from dataclasses import dataclass, field
import math
from collections import deque, defaultdict

import itertools
import functools


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = list(f.readlines())

    with Timer("part 1"):
        def get_decimal(snafu):
            VALS = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
            return sum(VALS[c]*(5**i) for i, c in enumerate(snafu[::-1]))
        total = sum(get_decimal(line.strip()) for line in lines)
        print("part 1 decimal:", total)

        def addb5(result, n, i):
            if len(result) == i+1:
                n += int(result.pop()) # this must be one
            LU = {0: "0", 1: "1", 2: "2", 3: "=1", 4: "-1", 5: "01"}
            result.extend(LU[n])

        remaining = total
        i, result = 0, []
        while remaining > 0:
            addb5(result, remaining % 5, i)
            remaining //= 5
            i += 1
        
        snafu = ''.join(result[::-1])
        assert get_decimal(snafu) == total
        print("Part 1 SNAFU:", snafu)


if __name__ == '__main__':
    main()
