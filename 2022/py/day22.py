from typing import *
from timer import Timer
import copy
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
            lines = [line[:-1] for line in f.readlines()]


    with Timer("part 1"):
        instrs = lines[-1]
        grid = lines[:-2]

        tokens = []
        i = 0
        while i < len(instrs):
            if instrs[i].isnumeric():
                j = i+1
                while j < len(instrs) and instrs[j].isnumeric():
                    j += 1
                tokens.append(instrs[i:j])
                i = j
            else:
                tokens.append(instrs[i])
                i += 1
        
        turn = [
            # dy, dx
            (0, 1), # right
            (1, 0), # down
            (0, -1), # left
            (-1, 0), # up
        ]
        H, W = len(grid), max(len(l) for l in grid)
        for i in range(len(grid)):
            if len(grid[i]) != W:
                grid[i] = grid[i] + " "*(W-len(grid[i]))

        x, y, f = 0, 0, 0
        while grid[y][x] == " ":
            x += 1

        for token in tokens:
            if token.isnumeric():
                dy, dx = turn[f]
                for _ in range(int(token)):
                    x2, y2 = (x+dx)%W, (y+dy)%H
                    while grid[y2][x2] == " ":
                        x2, y2 = (x2+dx)%W, (y2+dy)%H
                    if grid[y2][x2] == "#":
                        break
                    else: 
                        assert grid[y2][x2] == "."
                        x, y = x2, y2
            else:
                f = (f + {"L": -1, "R": 1}[token]) % 4

        print("part 1:", 1000*(y+1)+4*(x+1)+f)

    with Timer("part 2"):
        x, y, f = 0, 0, 0
        while grid[y][x] == " ":
            x += 1
        
        def correct(x, y, f, dx, dy):
            if y < 0:
                if 50 <= x < 100:
                    return 0, 150 + (x-50), 0
                elif 100 <= x < 150:
                    return x-100, 199, 3
                else:
                    assert False, (x, dx, y, dy)
            elif x >= W:
                if 0 <= y < 50:
                    return 99, 149-y, 2
                else:
                    assert False, (x, dx, y, dy)
            elif x < 0:
                if 100 <= y < 150:
                    return 50, 49-(y-100), 0 
                elif 150 <= y < 200:
                    return 50+(y-150), 0, 1
                else:
                    assert False, (x, dx, y, dy)
            elif y >= H:
                if 0 <= x < 50:
                    return 100+x, 0, 1
                else:
                    assert False, (x, dx, y, dy)
            elif 0 <= x < 50:
                if 0 <= y < 50:
                    return 0, 149-y, 0
                elif 50 <= y < 100:
                    if dx == -1:
                        return y-50, 100, 1
                    elif dy == -1:
                        return 50, 50+x, 0
                    else:
                        assert False, (x, dx, y, dy)
                else:
                    return x, y, f
            elif 100 <= x < 150:
                if 0 <= y < 50:
                    return x, y, f
                elif 50 <= y < 100:
                    if dy == 1:
                        return 99, 50 + (x-100), 2
                    elif dx == 1:
                        return 100+(y-50), 49, 3
                    else:
                        assert False, (x, dx, y, dy)
                elif 100 <= y < 150:
                    return 149, 49 - (y-100), 2
                else:
                    assert False (x, dx, y, dy)
            elif 50 <= x < 100:
                if y < 150:
                    return x, y, f
                else:
                    if dy == 1:
                        return 49, 150 + x-50, 2
                    elif dx == 1:
                        return 50 + y-150, 149, 3

            return x, y, f

        for token in tokens:
            if token.isnumeric():
                for _ in range(int(token)):
                    dy, dx = turn[f]
                    x2, y2, f2 = correct(x+dx, y+dy, f, dx, dy)
                    if grid[y2][x2] == "#":
                        break
                    else: 
                        assert grid[y2][x2] == "."
                        x, y, f = x2, y2, f2
            else:
                f = (f + {"L": -1, "R": 1}[token]) % 4
        print("part 2:", 1000*(y+1)+4*(x+1)+f)


if __name__ == '__main__':
    main()
