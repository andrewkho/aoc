from timer import Timer
import utils
from utils import get_input, Grid
from collections import defaultdict, Counter
import itertools
import bisect
import functools

import re


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        def get_next(vals):
            if all(x == 0 for x in vals):
                return 0
            nxt = [vals[i+1]-vals[i] for i in range(len(vals)-1)]
            return get_next(nxt) + vals[-1]

        result = 0
        for line in lines:
            vals = [int(x) for x in line.split(" ")]
            result += get_next(vals)

        print("part1:", result)

    with Timer("part 2"):
        def get_next(vals):
            if all(x == 0 for x in vals):
                return 0
            nxt = [vals[i+1]-vals[i] for i in range(len(vals)-1)]
            return vals[0] - get_next(nxt)

        result = 0
        for line in lines:
            vals = [int(x) for x in line.split(" ")]
            result += get_next(vals)

        print("part 2:", result)


if __name__ == '__main__':
    main()
