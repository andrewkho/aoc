import multiprocessing as mp
import random
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
        src, dst = None, None

        Y, X = len(lines), len(lines[0])
        for i in range(X):
            if lines[0][i] == ".":
                src = (0, i)
            if lines[Y-1][i] == ".":
                dst = (Y-1, i)


        slope_map = {">": [(0, 1)], "<": [(0, -1)], "v": [(1, 0)], "^": [(-1, 0)]}
        deltas = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            
        def get_graph(ignore_slopes=True):
            nodes = [src, dst]
            for j, line in enumerate(lines):
                for i, c in enumerate(line):
                    if c != ".":
                        continue
                    neighbours = []
                    for dj, di in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        if not 0 <= j+dj < Y:
                            continue
                        if not 0 <= i+di < X:
                            continue
                        if lines[j+dj][i+di] == "#":
                            continue
                        neighbours.append((j+dj, i+di))
                    if len(neighbours) > 2:
                        nodes.append((j, i))

            # build edges
            graph = {node: [] for node in nodes}
            for node in nodes:
                j, i = node
                for dj, di in deltas:
                    if not 0 <= j+dj < Y or not 0 <= i+di < X:
                        continue
                    if lines[j+dj][i+di] == "#":
                        continue
                    elif not ignore_slopes:
                        if (dj, di) not in slope_map.get(lines[j+dj][i+di], deltas):
                            continue

                    length = 1
                    y, x = j+dj, i+di
                    seen = {node, (y, x)}
                    while length == 1 or (y, x) not in nodes:
                        found = False
                        for dy, dx in deltas:
                            if (y+dy, x+dx) in seen or lines[y+dy][x+dx] == "#":
                                continue
                            elif not ignore_slopes:
                                if (dy, dx) not in slope_map.get(lines[y+dy][x+dx], deltas):
                                    continue
                            found, length, prev, (y, x) = True, length+1, (y, x), (y+dy, x+dx)
                            seen.add((y, x))
                            break
                        if not found:
                            break
                    if (y, x) in nodes:
                        graph[node].append(((y, x), length))
            return graph
        
        def dfs(pos=src, length=0):
            if pos == dst:
                return length
            best = 0
            for end, dlength in graph[pos]:
                if not visited[end]: 
                    visited[end] = True
                    best = max(best, dfs(end, length+dlength))
                    visited[end] = False
            return best

        graph = get_graph(False)
        visited = {k: False for k in graph}
        visited[src] = True
        print("part1:", dfs())

    with Timer("part 2"):
        graph = get_graph(True)
        visited = {k: False for k in graph}
        visited[src] = True
        print("part 2:", dfs())


if __name__ == '__main__':
    main()
