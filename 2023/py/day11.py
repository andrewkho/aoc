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
        result = 0
        galaxies = []
        for j, line in enumerate(lines):
            for i, c in enumerate(line):
                if c == "#":
                    galaxies.append((j, i))

        empty_rows = [True]*len(lines)
        empty_cols = [True]*len(lines[0])
        for j, i in galaxies:
            empty_rows[j] = False
            empty_cols[i] = False

        def f(expansion):
            total = 0
            for i, (sj, si) in enumerate(galaxies):
                for dj, di in galaxies[i+1:]:
                    for j in range(min(sj, dj), max(sj, dj)):
                        if empty_rows[j]:
                            total += expansion
                        else:
                            total += 1

                    for i in range(min(si, di), max(si, di)):
                        if empty_cols[i]:
                            total += expansion
                        else:
                            total += 1
            return total

        print("part1:", f(2))

    with Timer("part 2"):
        print("part 2:", f(1_000_000))


if __name__ == '__main__':
    main()
