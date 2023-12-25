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
        result = 0
        graph = defaultdict(list)
        for line in lines:
            left, right = line.split(": ")
            for o in right.split(" "):
                graph[left].append(o)
                graph[o].append(left)

        from scipy.sparse import csr_matrix

        from scipy.sparse.csgraph import maximum_flow
        adjacency = [[0]*len(graph) for _ in range(len(graph))]
        index = {node: i for i, node in enumerate(graph)}
        for node, edges in graph.items():
            for edge in edges:
                adjacency[index[node]][index[edge]] = 1

        m = csr_matrix(adjacency)
        def min_cut(src, dst):
            result = maximum_flow(m, src, dst)
            resid = m - result.flow
            # dfs
            visited = [0]*len(index)
            stack = [src]
            while stack:
                node = stack.pop()
                visited[node] = 1
                for i in range(len(index)):
                    if visited[i]:
                        continue
                    if resid[node, i] == 1:
                        stack.append(i)
            cut = []
            for node in range(len(visited)):
                if visited[node]:
                    for j in range(len(visited)):
                        if node == j or visited[j] or m[node, j] == 0:
                            continue
                        cut.append((node, j))
            return len(cut), sum(visited), len(visited) - sum(visited)
        
        # Just search until we find a min-cut of 3 edges
        result = None
        for i in range(len(index)):
            for j in range(i+1, len(index)):
                ncut, ns, nt = min_cut(i, j)
                if ncut == 3:
                    result = ns*nt
                    print("========")
                    print(ncut, i, j, ns, nt, ns * nt)
                    print("========")
                    break
            if result is not None:
                break

        print("part1:", result)


if __name__ == '__main__':
    main()
