import multiprocessing as mp
from typing import *
from timer import Timer
import utils
from utils import get_input, Grid
from collections import defaultdict, Counter
import itertools
import bisect
import functools
import copy

import re


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        Y, X = len(lines), len(lines[0])
        def get_load(lines):
            result = 0
            for j, line in enumerate(lines):
                result += sum(1 for c in line if c == "O")*(Y-j)
            return result

        def roll(grid, dirn):
            grid = [list(x) for x in grid]
            if dirn == "N":
                grid.append("#"*X)
                for i in range(X):
                    base = -1
                    stones = 0
                    for j in range(len(grid)):
                        if grid[j][i] == "#":
                            for jj in range(base+1, base+1+stones):
                                grid[jj][i] = "O"
                            for jj in range(base+1+stones, j):
                                grid[jj][i] = "."
                            base = j
                            stones = 0
                        elif grid[j][i] == "O":
                            stones += 1
                grid = grid[:-1]

            elif dirn == "S":
                grid = ["#"*X] + grid
                for i in range(X):
                    base = Y+1
                    stones = 0
                    for j in range(len(grid)-1, -1, -1):
                        if grid[j][i] == "#":
                            for jj in range(base-1, base-1-stones, -1):
                                grid[jj][i] = "O"
                            for jj in range(base-1-stones, j, -1):
                                grid[jj][i] = "."
                            base = j
                            stones = 0
                        elif grid[j][i] == "O":
                            stones += 1
                grid = grid[1:]

            elif dirn == "W":
                for j in range(Y):
                    grid[j] = grid[j] + ["#"]
                for j in range(Y):
                    base = -1
                    stones = 0
                    for i in range(X+1):
                        if grid[j][i] == "#":
                            for ii in range(base+1, base+1+stones):
                                grid[j][ii] = "O"
                            for ii in range(base+1+stones, i):
                                grid[j][ii] = "."
                            base = i
                            stones = 0
                        elif grid[j][i] == "O":
                            stones += 1
                for j in range(Y):
                    grid[j] = grid[j][:-1]

            elif dirn == "E":
                for j in range(Y):
                    grid[j] = ["#"] + grid[j]
                for j in range(Y):
                    base = X+1
                    stones = 0
                    for i in range(X+1-1, -1, -1):
                        if grid[j][i] == "#":
                            for ii in range(base-1, base-1-stones, -1):
                                grid[j][ii] = "O"
                            for ii in range(base-1-stones, i, -1):
                                grid[j][ii] = "."
                            base = i
                            stones = 0
                        elif grid[j][i] == "O":
                            stones += 1
                for j in range(Y):
                    grid[j] = grid[j][1:]
            else:
                raise ValueError(dirn)
            assert (len(grid), len(grid[0])) == (X, Y)
            grid = ["".join(x) for x in grid]
            return grid

        print("part1:", get_load(roll(lines, "N")))

    with Timer("part 2"):
        seen = {}
        i = 0
        cycle_length = -1
        while i < 1000000000:
            for dirn in "NWSE":
                lines = roll(lines, dirn)
            key = "\n".join(lines)
            if cycle_length == -1 and key in seen:
                # Cycle detected
                cycle_length = i-seen[key]
                i += ((1000000000 - i) // cycle_length ) * cycle_length
            else:
                seen[key] = i
            i += 1

        print("part 2:", get_load(lines))


if __name__ == '__main__':
    main()
