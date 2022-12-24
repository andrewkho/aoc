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
        blizzards = defaultdict(list)
        with open(infile, "r") as f:
            for j, line in enumerate(f.readlines()):
                for i, c in enumerate(line.strip()):
                    if c in "^<>v":
                        blizzards[c].append([i, j])
            H, W = j+1, i+1

    with Timer("part 1"):
        start = (1, 0)
        end = (W-2, H-1)
        grids = []
        def get_grid(t):
            if t < len(grids):
                return grids[t]
            assert t == len(grids), (t, len(grids))
            if t > 0:
                move()
            grid = [[0]*W for _ in range(H)]
            for i in range(W):
                grid[0][i] = 1
                grid[H-1][i] = 1
            for j in range(H):
                grid[j][0] = 1
                grid[j][W-1] = 1
            for x, y in [start, end]:
                grid[y][x] = 0
            for k, v in blizzards.items():
                for bx, by in v:
                    grid[by][bx] = 1
            grids.append(grid)
            return grids[t]
        
        def move():
            for k in "><":
                dx = {">": 1, "<": -1}[k]
                for el in blizzards[k]:
                    el[0] += dx
                    if el[0] == 0:
                        el[0] = W-2
                    elif el[0] == W-1:
                        el[0] = 1
            for k in "v^":
                dy = {"^": -1, "v": 1}[k]
                for el in blizzards[k]:
                    el[1] += dy
                    if el[1] == 0:
                        el[1] = H-2
                    elif el[1] == H-1:
                        el[1] = 1

        def bfs(start, end, t):
            dq = deque([(start[0], start[1], t)])
            best = 1e6
            seen = set()
            while len(dq) > 0:
                x, y, t = dq.popleft()
                grid = get_grid(t)
                
                if (x, y) == end:
                    best = min(t, best)
                    continue
                elif t + (abs(end[0]-x) + abs(end[1]-y)) >= best:
                    continue
                elif grid[y][x] == 1:
                    continue

                for dx, dy in [[1, 0], [-1, 0], [0, 1], [0, -1], [0, 0]]:
                    if not (0 <= x+dx < W and 0 <= y+dy < H):
                        continue
                    if (x+dx, y+dy, t+1) in seen:
                        continue
                    seen.add((x+dx, y+dy, t+1))
                    dq.append((x+dx, y+dy, t+1))
            return best
        
        x = bfs(start, end, 0)
        print("part 1:", x)

    with Timer("part 2"):
        x = bfs(end, start, x)
        x = bfs(start, end, x)
        print("part 2:", x)


if __name__ == '__main__':
    main()
