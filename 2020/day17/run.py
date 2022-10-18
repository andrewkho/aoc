import fire
from typing import *
import re
import itertools
from collections import deque

from dataclasses import dataclass, field
import numpy as np


def _active_neighbours(active, coord):
    c = 0
    iterator = itertools.product(
        *[range(-1, 2) for _ in coord]
    )
    for delta in iterator:
        if all(d == 0 for d in delta):
            continue

        if tuple(c + d for c, d in zip(coord, delta)) in active:
            c += 1

    return c


def _part_one(data):
    n_cycles = 6

    a = data[0]
    active = data[1]


    for i in range(n_cycles):
        b = dict()
        bctive = set()

        # Handle active case
        for coord in active:
            if _active_neighbours(active, coord) in (2, 3):
                b[coord] = '#'
                bctive.add(coord)

        processed = set()
        # Handle inactive cases flipping
        for coord in active:
            iterator = itertools.product(
                *[range(-1, 2) for _ in coord]
            )
            for delta in iterator:
                new_coord = tuple(c+d for c, d in zip(coord, delta))
                # Only consider inactive
                if new_coord in active:
                    continue
                # Skip if already processed
                if new_coord in processed:
                    continue

                if _active_neighbours(active, new_coord) == 3:
                    b[new_coord] = '#'
                    bctive.add(new_coord)

                processed.add(new_coord)
        a = b
        active = bctive

    return len(active)


def _parse_lines(lines, dims):
    a = dict()
    active = set()

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            coord = [x, y]
            for d in range(dims-2):
                coord.append(0)
            coord = tuple(coord)
            a[coord] = c
            if c == '#':
                active.add(coord)

    return a, active


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)

    if part == 1:
        data = _parse_lines(lines, 3)
        r = _part_one(data)
        print('part 1: ' + str(r))
    elif part == 2:
        data = _parse_lines(lines, 4)
        r = _part_one(data)
        print('part 2: ' + str(r))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

