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


def get_area(lines, part=1):
    pos = (0, 0)
    segments = []
    lr, ud = [], []
    for line in lines:
        m = re.match(r"^(U|R|L|D) ([0-9]+) \((.*)\)$", line)
        dirn = m.groups()[0]
        steps = int(m.groups()[1])
        if part == 2:
            colour = m.groups()[2][1:]
            dirn = "RDLU"[int(colour[-1])]
            steps = int(colour[:-1], 16)

        dj, di = {
            "R": [0, 1],
            "L": [0, -1],
            "U": [-1, 0],
            "D": [1, 0]
        }[dirn]
        end = (pos[0] + dj*steps, pos[1] + di*steps)
        segments.append((pos, end, dirn))
        if dirn in "UD":
            ud.append((pos[1], pos[0], end[0], dirn))
        else:
            lr.append((pos[0], pos[1], end[1], dirn))
        pos = end

    ud = sorted(ud)
    lr = sorted(lr)
    def scanline(j, edges):
        flip = 0
        prev_dirn, prev_i = None, None
        result = 0
        for i, j0, j1, dirn in ud:
            if not min(j0, j1) <= j <= max(j0, j1):
                continue
            result += 1
            if dirn == "U":
                if prev_dirn != "U":
                    flip += 1
                    if flip == 0 and (prev_i, i) not in edges:
                        result += i - prev_i - 1
                prev_dirn, prev_i = dirn, i
            elif dirn == "D":
                if prev_dirn != "D":
                    flip -= 1
                    if flip == 0 and (prev_i, i) not in edges:
                        result += i - prev_i - 1
                prev_dirn, prev_i = dirn, i
        assert flip == 0, (flip, j)
        return result

    result = 0
    idx = 0
    j = lr[idx][0]
    prev_j = j
    edges = set()
    while lr[idx][0] == j:
        _, i0, i1, _ = lr[idx]
        edges.add((min(i0, i1), max(i0, i1)))
        result += max(i0, i1) - min(i0, i1) - 1
        idx += 1
    result += scanline(j, edges)

    while idx < len(lr):
        # Filling
        j = lr[idx][0]
        assert j-prev_j-1 >= 0, (j, prev_j, idx)
        if j - prev_j - 1 > 0:
            result += scanline(j-1, set()) * (j-prev_j-1)
        edges = set()
        while idx < len(lr) and lr[idx][0] == j:
            _, i0, i1, _ = lr[idx]
            edges.add((min(i0, i1), max(i0, i1)))
            result += max(i0, i1) - min(i0, i1) - 1
            idx += 1
        result += scanline(j, edges)
        prev_j = j
    return result


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())
    
    with Timer("part 1"):
        print("part1:", get_area(lines, part=1))

    with Timer("part 2"):
        print("part 2:", get_area(lines, part=2))


if __name__ == '__main__':
    main()
