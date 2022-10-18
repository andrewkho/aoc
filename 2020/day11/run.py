import fire
from typing import *
import re
import numpy as np
from collections import deque
from dataclasses import dataclass, field


def _step(a, seats):
    h, w = a.shape

    changes = 0
    b = np.zeros(a.shape)

    for i, j in seats:
        s = a[j-1:j+2,i-1:i+2].sum()

        m = a[j, i]

        if m == 0 and s == 0:
            b[j, i] = 1
            changes += 1
        elif m == 1 and s >= (4+1):
            b[j, i] = 0
            changes += 1
        else:
            b[j, i] = m

    return b, changes



def _part_one(data, seats):
    i = 0
    while True:
        if i % 100 == 0:
            print(f"step {i}")

        data, c = _step(data, seats)
        #_print(data, seats)
        if c == 0:
            return data
        i += 1


def _step_adj(a, seats, adj):
    h, w = a.shape

    changes = 0
    b = np.zeros(a.shape)

    a_flat = a.reshape([1, h*w])

    for i, j in seats:
        y = j*w + i
        s = a_flat.dot(adj[y,:])

        m = a[j, i]

        if m == 0 and s == 0:
            b[j, i] = 1
            changes += 1
        elif m == 1 and s >= 5:
            b[j, i] = 0
            changes += 1
        else:
            b[j, i] = m

    return b, changes

def _part_two(data, seats, adj):
    i = 0
    while True:
        if i % 100 == 0:
            print(f"step {i}")

        data, c = _step_adj(data, seats, adj)
        #_print(data, seats)
        if c == 0:
            return data
        i += 1


def _process_lines(lines):
    w = len(lines[0].strip())
    h = len(lines)

    a = np.zeros([h+2, w+2])

    seats = []

    for j, line in enumerate(lines):
        for i, char in enumerate(line.strip()):
            if char == 'L':
                a[j+1, i+1] = 0
                seats.append((i+1, j+1))
            elif char == '#':
                a[j+1, i+1] = 1
                seats.append((i+1, j+1))
            elif char == '.':
                a[j+1, i+1] = 0
            else:
                raise ValueError('char: {char}')

    return a, seats


def _make_adjacency(a, seats):
    h, w = a.shape
    n = h*w

    adj = np.zeros([n, n])

    seats = set(seats)

    for i, j in seats:
        x = j*w + i

        # up
        for delta in range(1, j):
            if (i, (j-delta)) in seats:
                y = (j-delta)*w + i
                adj[x, y] = 1
                adj[y, x] = 1
                break

        # down
        for delta in range(1, h-j):
            if (i, (j+delta)) in seats:
                y = (j+delta)*w + i
                adj[x, y] = 1
                adj[y, x] = 1
                break

        # left
        for delta in range(1, i):
            if ((i-delta), j) in seats:
                y = j*w + i-delta
                adj[x, y] = 1
                adj[y, x] = 1
                break

        # right
        for delta in range(1, w-i):
            if ((i+delta), j) in seats:
                y = j*w + i+delta
                adj[x, y] = 1
                adj[y, x] = 1
                break

        # up-left
        for delta in range(1, min(j, i)):
            if ((i-delta), (j-delta)) in seats:
                y = (j-delta)*w + i-delta
                adj[x, y] = 1
                adj[y, x] = 1
                break

        # up-right
        for delta in range(1, min(j, w-i)):
            if ((i+delta), (j-delta)) in seats:
                y = (j-delta)*w + i+delta
                adj[x, y] = 1
                adj[y, x] = 1
                break

        # down-left
        for delta in range(1, min(h-j, i)):
            if ((i-delta), (j+delta)) in seats:
                y = (j+delta)*w + i-delta
                adj[x, y] = 1
                adj[y, x] = 1
                break

        # down-right
        for delta in range(1, min(h-j, w-i)):
            if ((i+delta), (j+delta)) in seats:
                y = (j+delta)*w + i+delta
                adj[x, y] = 1
                adj[y, x] = 1
                break

    return adj


def _print(a, seats):
    h, w = a.shape
    show = []
    seats = set(seats)
    for j in range(h):
        line = []
        for i in range(w):
            if (i,j) not in seats:
                line.append('.')
            else:
                if a[j,i] == 0:
                    line.append('L')
                elif a[j,i] == 1:
                    line.append('#')
        line.append('\n')
        show.append(''.join(line))

    print(''.join(show))


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)
    data, seats = _process_lines(lines)
    adj = _make_adjacency(data, seats)
    _print(data, seats)

    print(f"data: {len(data)} lines: {len(lines)}")
    print(data)

    if part == 1:
        r = _part_one(data, seats)
        _print(r, seats)
        print('part 1: ' + str(r.sum()))
    elif part == 2:
        r = _part_two(data, seats, adj)
        _print(r, seats)
        print('part 2: ' + str(r.sum()))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

