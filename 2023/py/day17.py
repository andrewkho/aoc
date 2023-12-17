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
        def dijkstra(min_steps, max_steps):
            pos = (0, 0)
            pq = [(0, 0, 0, 0, 0, 0)]
            seen = set()
            Y, X = len(lines), len(lines[0])
            while pq:
                cost, j, i, count, prev_dj, prev_di = heapq.heappop(pq)

                if (j, i) == (Y-1, X-1) and count >= min_steps-1:
                    return cost

                for dj, di in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
                    if not 0 <= j+dj < Y:
                        continue
                    elif not 0 <= i+di < X:
                        continue
                    
                    if cost > 0 and count < min_steps-1 and (dj, di) != (prev_dj, prev_di):
                        continue

                    if (dj, di) == (-prev_dj, -prev_di):
                        continue
                    elif (dj, di) == (prev_dj, prev_di):
                        if count+1 == max_steps:
                            continue
                        dc = count+1
                    else:
                        dc = 0

                    if (j+dj, i+di, dc, dj, di) in seen:
                        continue

                    seen.add((j+dj, i+di, dc, dj, di))

                    heapq.heappush(pq, (
                        cost + int(lines[j+dj][i+di]),
                        j+dj, i+di,
                        dc,
                        dj, di,
                    ))
        
        print("part1:", dijkstra(0, 3))

    with Timer("part 2"):
        print("part 2:", dijkstra(4, 10))


if __name__ == '__main__':
    main()
