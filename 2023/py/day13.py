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
        result = 0
        def f(grid, prev=None):
            j = 1
            grid_result = 0
            found = 0
            while j < len(grid):
                if grid[j] == grid[j-1]:
                    dj = 1
                    while j+dj < len(grid) and j-1-dj >= 0:
                        if grid[j+dj] != grid[j-1-dj]:
                            break
                        dj += 1
                    if j+dj == len(grid) or j-1-dj == -1:
                        if j != prev:
                            return j
                j += 1
            return None

        grid = []
        lines.append("")
        for line in lines:
            if line.strip() == "":
                v = f(grid)
                if v is not None:
                    result += v*100
                else:
                    tx = []
                    for i in range(len(grid[0])):
                        tx.append("".join(grid[j][i] for j in range(len(grid))))
                    result += f(tx)
                grid = []
            else:
                grid.append(line)

        print("part1:", result)


    with Timer("part 2"):
        def search(grid):
            prev_v = f(grid)
            for j in range(len(grid)):
                orig = grid[j]
                line = list(grid[j])
                for i in range(len(line)):
                    line[i] = {"#": ".", ".": "#"}[line[i]]
                    grid[j] = "".join(line)
                    v = f(grid, prev_v)
                    if v is not None:
                        return v
                    line[i] = {"#": ".", ".": "#"}[line[i]]
                grid[j] = orig

            return None
            
        result = 0
        reflections = []
        grid = []
        for line in lines:
            if line.strip() == "":
                v = search(grid.copy())
                if v is not None:
                    result += v*100
                else:
                    tx = []
                    for i in range(len(grid[0])):
                        tx.append("".join(grid[j][i] for j in range(len(grid))))
                    result += search(tx)
                grid = []
            else:
                grid.append(line)
        print("part 2:", result)


if __name__ == '__main__':
    main()
