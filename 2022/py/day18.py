from typing import *
from timer import Timer
import copy
import re
from dataclasses import dataclass, field
import math
from collections import deque, defaultdict

import itertools
import functools


NEIS = [
    [-1, 0, 0],
    [1, 0, 0],
    [0, -1, 0],
    [0, 1, 0],
    [0, 0, -1],
    [0, 0, 1],
]

def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    pts = []
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            for line in f.readlines():
                pts.append(tuple(map(int, line.strip().split(','))))
    
    with Timer("part 1"):
        hm = set(pts)
        total = 0
        for x, y, z in pts:
            for dx, dy, dz in NEIS:
                if (x+dx, y+dy, z+dz) not in hm:
                    total += 1
        print("part 1:", total)

    with Timer("part 2"):
        mx = [-1e6, -1e6, -1e6]
        mn = [1e6, 1e6, 1e6]
        for pt in pts:
            for i in range(3):
                mn[i] = min(pt[i], mn[i])
                mx[i] = max(pt[i], mx[i])

        q = [(mn[0]-1, mn[1]-1, mn[2]-1)]
        outside = set(q)
        while q:
            x, y, z = q.pop()
            for dx, dy, dz in NEIS:
                if not all([
                        mn[0]-1 <= x+dx < mx[0]+2, 
                        mn[1]-1 <= y+dy < mx[1]+2, 
                        mn[2]-1 <= z+dz < mx[2]+2]):
                    continue
                if (x+dx, y+dy, z+dz) in outside:
                    continue
                if (x+dx, y+dy, z+dz) in hm:
                    continue
                outside.add((x+dx, y+dy, z+dz)) 
                q.append((x+dx, y+dy, z+dz))

        total = 0
        for x, y, z in pts:
            for dx, dy, dz in NEIS:
                if (x+dx, y+dy, z+dz) in outside:
                    total += 1
        print("part 2:", total)


if __name__ == '__main__':
    main()
