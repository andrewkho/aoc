import multiprocessing as mp
from typing import *
from timer import Timer
import utils
from utils import get_input, Grid
from collections import defaultdict, Counter, deque
from dataclasses import dataclass, field
import itertools
import bisect
import functools
import copy
import heapq

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
        start = None
        for j, line in enumerate(lines):
            for i, c in enumerate(line):
                if c == "S":
                    start = (j, i)
                    break
            if start is not None:
                break
        
        positions = [set() for _ in range(65)]
        positions[0].add(start)
        for step in range(1, 65):
            for cur in positions[step-1]:
                j, i = cur
                for dj, di in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    if not 0 <= j+dj < len(lines):
                        continue
                    if not 0 <= i+di < len(lines[0]):
                        continue
                    if lines[j+dj][i+di] == "#":
                        continue
                    positions[step].add((j+dj, i+di))

        print("part1:", len(positions[64]))

    with Timer("part 2"):
        Y, X = len(lines), len(lines[0])
        positions = [defaultdict(set), defaultdict(set)]
        positions[1][start] = {(0, 0)}

        @functools.lru_cache()
        def get_max_changes(j, i):
            changes = []
            neighbours = []
            for dj, di in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                if lines[(j+dj)%Y][(i+di)%X] == "#":
                    continue
                neighbours.append(((j+dj)%Y, (i+di)%X))
                changes.append(((j+dj)//Y, (i+di)//X))
            return tuple(neighbours), tuple(changes)
            
        # We end exactly at the end of 1 grid, let's see if
        # there's a pattern we can extrapolate
        # 
        # Simulate for a few grids to see the pattern on edges
        def tally(step) -> int:
            grid_counts = defaultdict(int)
            for (i, j), grids in positions[step%2].items():
                for grid in grids:
                    grid_counts[grid] += 1
            return sum(grid_counts.values())

        prev_total = 0
        prev_delta = 0
        for step in range(65 + 7 * 131 + 1):
            positions[step%2].clear()
            for (j, i), grids in positions[1-step%2].items():
                neighbours, changes = get_max_changes(j, i)
                for (nj, ni), (dgj, dgi) in zip(neighbours, changes):
                    for gj, gi in grids:
                        positions[step%2][(nj, ni)].add((gj+dgj, gi+dgi))
            if (step+1 - 65) % 131 == 0:
                total = tally(step)
                delta = total - prev_total
                ddelta = delta - prev_delta
                print(f"{step+1=}, {(step+1-65)//131=}, {total=}, {delta=}, {ddelta=}")
                prev_total = total
                prev_delta = delta

        # step+1=65, (step+1-65)//131=0, total=3770, delta=3770, ddelta=3770
        # step+1=196, (step+1-65)//131=1, total=33665, delta=29895, ddelta=26125
        # step+1=327, (step+1-65)//131=2, total=93356, delta=59691, ddelta=29796
        # step+1=458, (step+1-65)//131=3, total=182843, delta=89487, ddelta=29796
        # step+1=589, (step+1-65)//131=4, total=302126, delta=119283, ddelta=29796
        # step+1=720, (step+1-65)//131=5, total=451205, delta=149079, ddelta=29796
        # ...
        # We use the initial condiitons and change per step to fast-forward
        x0 = 3770
        x1 = 29895
        dx1 = 29796
        grid_steps = (26501365-65) // 131
        for step in range(grid_steps):
            x0 += x1
            x1 += dx1

        print("part 2:", x0)


if __name__ == '__main__':
    main()
