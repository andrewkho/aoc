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
        paths = []
        with open(infile, "r") as f:
            for line in f.readlines():
                paths.append([eval(x) for x in line.strip().split(" -> ")])

    mx = [-float('inf'), -float('inf')]
    for path in paths:
        for x, y in path:
            mx[0] = max(mx[0], x)
            mx[1] = max(mx[1], y)

    with Timer("part 1"):
        grid = {}
        for path in paths:
            for i in range(len(path)-1):
                if path[i][0] == path[i+1][0]:
                    x = path[i][0]
                    y0 = min(path[i][1], path[i+1][1])
                    y1 = max(path[i][1], path[i+1][1])
                    for y in range(y0, y1+1):
                        grid[y, x] = '#'
                else:
                    y = path[i][1]
                    x0 = min(path[i][0], path[i+1][0])
                    x1 = max(path[i][0], path[i+1][0])
                    for x in range(x0, x1+1):
                        grid[y, x] = '#'

        start = (500, 0)
        def drop():
            x, y = start
            while True:
                if not y < mx[1]:
                    return False
                if (y+1, x) not in grid:
                    y += 1
                elif (y+1, x-1) not in grid:
                    y += 1
                    x -= 1
                elif (y+1, x+1) not in grid:
                    y += 1
                    x += 1
                else:
                    break

            grid[y, x] = "o"
            return True

        total = 0
        while drop():
            total += 1

        print("part 1:", total)

    with Timer("part 2"):
        def drop():
            x, y = start
            if (y, x) in grid:
                return False

            while True:
                if not y < mx[1]+1:
                    break
                if (y+1, x) not in grid:
                    y += 1
                elif (y+1, x-1) not in grid:
                    y += 1
                    x -= 1
                elif (y+1, x+1) not in grid:
                    y += 1
                    x += 1
                else:
                    break

            grid[y, x] = "o"
            return True

        while drop():
            total += 1

        print("part 2:", total)


if __name__ == '__main__':
    main()
