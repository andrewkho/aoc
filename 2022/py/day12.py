from typing import *
from timer import Timer
import copy
import re
from dataclasses import dataclass, field
import math
from collections import deque


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            M = []
            start = None
            end = None
            for i, line in enumerate(f.readlines()):
                row = []
                for j, c in enumerate(line.strip()):
                    if c == 'S':
                        row.append(0)
                        start = (i, j)
                    elif c == 'E':
                        row.append(ord('z') - ord('a'))
                        end = (i, j)
                    else:
                        row.append(ord(c) - ord('a'))
                M.append(row)

    def bfs(i, j, stop_condition, step_condition) -> int:
        dq = deque()
        dq.append((i, j, 0))
        seen = [[False]*len(M[0]) for _ in range(len(M))]
        seen[i][j] = True

        while len(dq) > 0:
            i, j, steps = dq.popleft()
            if stop_condition(i, j):
                return steps
            for di, dj in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                if not (0 <= i+di < len(M)) or not (0 <= j+dj < len(M[0])):
                    continue
                if seen[i+di][j+dj]:
                    continue
                if step_condition(i, j, di, dj):
                    continue
                seen[i+di][j+dj] = True
                dq.append((i+di, j+dj, steps+1))

        return None 

    with Timer("part 1"):
        bst = bfs(
            start[0], start[1], 
            lambda i, j: (i, j) == end,
            lambda i, j, di, dj: M[i+di][j+dj] - M[i][j] > 1,
        )
        print("part 1:", bst)

    with Timer("part 2"):
        bst = bfs(
            end[0], end[1], 
            lambda i, j: M[i][j] == 0,
            lambda i, j, di, dj: M[i+di][j+dj] - M[i][j] < -1,
        )
        print("part 2:", bst)


if __name__ == '__main__':
    main()
