import math
import fire
from typing import *
import re
import itertools
from collections import deque, defaultdict

from dataclasses import dataclass, field
import numpy as np



DIRECTIONS = {
    'e':  (0, 1),
    'se': (1, 1),
    'sw': (1, 0),
    'w':  (0, -1),
    'nw': (-1, -1),
    'ne': (-1, 0),
}

def _initialize(data):
    tiles = defaultdict(lambda: 0)
    for dirs in data:
        pos = [0, 0]
        for dir in dirs:
            mv = DIRECTIONS[dir]
            pos[0] += mv[0]
            pos[1] += mv[1]

        tiles[tuple(pos)] = 1 - tiles[tuple(pos)]

    return tiles


def _part_one(data):
    tiles = _initialize(data)

    return sum(tiles.values())
    

def _active_neighbours(active, coord):
    return sum(
        1 for d in DIRECTIONS.values()
        if (coord[0] + d[0], coord[1] + d[1]) in active
    )


def _part_two(data, steps):
    tiles = _initialize(data)
    black = {c for c, v in tiles.items() if v == 1}
    print(f'initial: {len(black)}')

    for _ in range(steps):
        new_black = set()

        # Check black
        for coord in black:
            n = _active_neighbours(black, coord)
            if n == 0 or n > 2:
                continue # not white
            else:
                new_black.add(coord) # remains black

        # Now check white
        visited = set()
        for coord in black:
            for delta in DIRECTIONS.values():
                nc = (coord[0] + delta[0], coord[1] + delta[1])
                if nc in black or nc in visited:
                    continue # currently black so continue
                visited.add(nc)
                if _active_neighbours(black, nc) == 2:
                    new_black.add(nc)

        black = new_black
        print(f'day {_}: {len(black)}')

    return len(black)


def _parse_line(line):
    dirs = []

    i = 0
    while True:
        if line[i] in ('e', 'w'):
            dirs.append(line[i])
            i += 1
        elif line[i] in ('s', 'n'):
            dirs.append(line[i:i+2])
            i += 2
        if i >= len(line.strip()):
            break

    assert ''.join(dirs) == line.strip()

    return dirs
    

def run(fname: str, part: int, steps: int=100):
    with open(fname, 'r') as f:
        lines = f.readlines()

    data = [_parse_line(line) for line in lines]

    print(str(data))

    if part == 1:
        r = _part_one(data)
        print('part 1: ' + str(r))
    elif part == 2:
        r = _part_two(data, steps)
        print('part 2: ' + str(r))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

