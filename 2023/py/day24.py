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


@dataclass
class Vector:
    x: Tuple[int]
    u: Tuple[int]


def intersection(a, b):
    x1, x2 = a.x[0], a.x[0] + a.u[0]
    y1, y2 = a.x[1], a.x[1] + a.u[1]
    x3, x4 = b.x[0], b.x[0] + b.u[0]
    y3, y4 = b.x[1], b.x[1] + b.u[1]
    if ((x1-x2)*(y3-y4) - (x3-x4)*(y1-y2)) == 0:
        u1denom = (a.u[0]**2 + a.u[1]**2)**0.5
        u1norm = (a.u[0] / u1denom, a.u[1] / u1denom)
        u2denom = (b.u[0]**2 + b.u[1]**2)**0.5
        u2norm = (b.u[0] / u2denom, b.u[1] / u2denom)
        return None
    t = ((x1-x3)*(y3-y4) - (x3-x4)*(y1-y3)) / ((x1-x2)*(y3-y4) - (x3-x4)*(y1-y2))
    u = ((x1-x3)*(y1-y2) - (x1-x2)*(y1-y3)) / ((x1-x2)*(y3-y4) - (x3-x4)*(y1-y2))

    if t < 0 or u < 0:
        return None
    return (x1 + t*(x2-x1), y1+t*(y2-y1))


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        vectors = []
        for line in lines:
            pos, vel = line.split(" @ ")
            vectors.append(
                Vector(
                    tuple(int(x) for x in pos.split(", ")),
                    tuple(int(x) for x in vel.split(", ")),
                )
            )

        result = 0
        for i in range(len(vectors)):
            a = vectors[i]
            for j in range(i+1, len(vectors)):
                b = vectors[j]
                ix = intersection(a, b)
                if ix is not None:
                    if ((200000000000000 <= ix[0] <= 400000000000000) and 
                        (200000000000000 <= ix[1] <= 400000000000000)):
                        result += 1

        print("part1:", result)

    with Timer("part 2"):
        # Set up 6 equations in 6 unknowns and solve
        # with unknown X = (x 0, y 1, z 2, u 3 , v 4, w 5)
        import numpy as np
        def get_coeffs(a, b):
            xi, yi, zi = a.x
            ui, vi, wi = a.u
            xj, yj, zj = b.x
            uj, vj, wj = b.u

            m = np.zeros((3, 6), dtype=np.int64)
            b = np.zeros(3, dtype=np.int64)

            # Miss 0, 3
            m[0, 5], m[0, 1], m[0, 4], m[0, 2] = yi-yj, wi-wj, -(zi-zj), -(vi-vj)
            b[0] = yi*wi - zi*vi - yj*wj + zj*vj

            # Miss 1, 4
            m[1, 3], m[1, 2], m[1, 5], m[1, 0] = zi-zj, ui-uj, -(xi-xj), -(wi-wj)
            b[1] = zi*ui - wi*xi - zj*uj + wj*xj

            # Miss 2, 5
            m[2, 4], m[2, 0], m[2, 3], m[2, 1] = xi-xj, vi-vj, -(yi-yj), -(ui-uj)
            b[2] = xi*vi - yi*ui - xj*vj + yj*uj
            return m, b

        for i in range(len(vectors)-4):
            m0, b0 = get_coeffs(vectors[i], vectors[i+1])
            m1, b1 = get_coeffs(vectors[i+2], vectors[i+3])
            
            m = np.concatenate([m0, m1], axis=0)
            b = np.concatenate([b0, b1], axis=0)

            # If condition number is too large, don't solve
            # we're at the limits of machine precision here with
            # roundoff errors in the range of 1e-1, however 1e13
            # gives the same result for my inputs
            if np.linalg.cond(m) > 1e13:
                continue

            x = np.linalg.solve(m, b)
            print(x[:3] - x[:3].round().astype(np.int64))
            result = x.round().astype(np.int64)[0:3].sum()
            print("part 2:", result)


if __name__ == '__main__':
    main()
