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
        pos = set()
        with open(infile, "r") as f:
            for j, line in enumerate(f.readlines()):
                for i, c in enumerate(line.strip()):
                    if c == "#":
                        pos.add((i, j))

    with Timer("part 1"):
        checks = [
            ((-1, -1), (0, -1), (1, -1)),
            ((-1, 1),  (0, 1),  (1, 1)),
            ((-1, -1), (-1, 0), (-1, 1)),
            ((1, -1),  (1, 0),  (1, 1)),
        ]
        nei8 = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0),           (1, 0),
            (-1, 1),  (0, 1),  (1, 1),
        ]
        def step(n, pos):
            proposed = dict()
            counts = defaultdict(lambda: 0)
            for x, y in pos:
                found = False
                if any((x+dx, y+dy) in pos for dx, dy in nei8):
                    for i in range(4):
                        if all((x+dx, y+dy) not in pos
                                for dx, dy in checks[(n+i)%4]):
                            dx, dy = checks[(n+i)%4][1]
                            proposed[x, y] = (x+dx, y+dy)
                            counts[x+dx, y+dy] += 1
                            found = True
                            break

                if not found:
                    proposed[x, y] = (x, y)
                    counts[x, y] += 1
            
            # resolve
            newpos = set()
            for cur, (x, y) in proposed.items():
                if counts[x, y] == 1:
                    newpos.add((x, y))
                else:
                    newpos.add(cur)
            return newpos

        def show(pos):
            mini, maxi = [float('inf'), float('inf')], [-float('inf'), -float('inf')]    
            for x, y in pos:
                mini[0] = min(mini[0], x)
                maxi[0] = max(maxi[0], x)
                mini[1] = min(mini[1], y)
                maxi[1] = max(maxi[1], y)
            for j in range(mini[0], maxi[0]+1):
                line = []
                for i in range(mini[1], maxi[1]+1):
                    if (i, j) in pos:
                        line.append("#")
                    else:
                        line.append(".")
                print(''.join(line))
        
        for n in range(10):
            pos = step(n, pos)
        mini, maxi = [float('inf'), float('inf')], [-float('inf'), -float('inf')]    
        for x, y in pos:
            mini[0] = min(mini[0], x)
            maxi[0] = max(maxi[0], x)
            mini[1] = min(mini[1], y)
            maxi[1] = max(maxi[1], y)
        print("part 1:", (1+maxi[1]-mini[1])*(1+maxi[0]-mini[0]) - len(pos))

    with Timer("part 2"):
        for n in range(10, 1000):
            newpos = step(n, pos)
            if newpos == pos:
                break
            pos = newpos
        print("part 2:", n+1)


if __name__ == '__main__':
    main()
