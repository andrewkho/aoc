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

import re


@dataclass
class Beam:
    y: int
    x: int
    dirn: Tuple[int] = field(default_factory=lambda: (0, 1))

    def clone(self):
        return Beam(self.y, self.x, self.dirn)

    def __hash__(self):
        return hash(hash(hash(self.dirn) + self.y) + self.x)

    def __equals__(self, o):
        return self.y == o.y and self.x == o.x and self.dirn == o.dirn


def get_energy(beams, lines):
    seen = set()
    cache = {}
    hits = [[0]*len(lines[0]) for _ in range(len(lines))]
    while True:
        key = frozenset(beams)
        if key in seen:
            break
        seen.add(key)
        if key in cache:
            next_beams = cache[key]
        else:
            next_beams = set()
            for beam in beams:
                n = beam.clone()
                n.y += n.dirn[0]
                n.x += n.dirn[1]
                if not (0 <= n.y < len(lines)):
                    continue
                elif not (0 <= n.x < len(lines[0])):
                    continue
                hits[n.y][n.x] += 1
                c = lines[n.y][n.x]
                if c == ".":
                    pass
                elif c == "|":
                    if n.dirn[1] != 0:
                        n2 = n.clone()
                        n.dirn = (1, 0)
                        n2.dirn = (-1, 0)
                        next_beams.add(n2)
                elif c == "-":
                    if n.dirn[0] != 0:
                        n2 = n.clone()
                        n.dirn = (0, 1)
                        n2.dirn = (0, -1)
                        next_beams.add(n2)
                elif c == "\\":
                    if n.dirn[0] == 1:
                        n.dirn = (0, 1)
                    elif n.dirn[0] == -1:
                        n.dirn = (0, -1)
                    elif n.dirn[1] == 1:
                        n.dirn = (1, 0)
                    elif n.dirn[1] == -1:
                        n.dirn = (-1, 0)
                elif c == "/":
                    if n.dirn[0] == 1:
                        n.dirn = (0, -1)
                    elif n.dirn[0] == -1:
                        n.dirn = (0, 1)
                    elif n.dirn[1] == 1:
                        n.dirn = (-1, 0)
                    elif n.dirn[1] == -1:
                        n.dirn = (1, 0)
                next_beams.add(n)
            cache[key] = frozenset(next_beams)

        beams = next_beams

    result = sum(
        sum(1 for x in hit if x > 0)
        for hit in hits
    )
    return result


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())
    
    with Timer("part 1"):
        beams = {Beam(0, -1, (0, 1))}
        print("part1:", get_energy(beams, lines))

    with Timer("part 2"):
        energies = []
        tasks = []
        tasks += [({Beam(j, -1, (0, 1))}, lines) for j in range(len(lines))]
        tasks += [({Beam(j, len(lines[0]), (0, -1))}, lines) for j in range(len(lines))]
        tasks += [({Beam(-1, i, (1, 0))}, lines) for i in range(len(lines[0]))]
        tasks += [({Beam(len(lines), i, (-1, 0))}, lines) for i in range(len(lines[0]))]
        with mp.Pool(12) as pool:
            energies += pool.starmap(get_energy, tasks)

        print("part 2:", max(energies))


if __name__ == '__main__':
    main()
