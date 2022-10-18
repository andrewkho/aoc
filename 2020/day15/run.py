import fire
from typing import *
import re
import itertools
from collections import deque

from dataclasses import dataclass, field
import numpy as np


def _part_one(data, stop):
    last = dict()
    l = None
    for turn, num in enumerate(data):
        last[num] = turn
        l = num

    while True:
        if l not in last:
            next = 0
        else:
            next = turn - last[l]

        last[l] = turn
        turn += 1
        l = next
        if turn+1 == stop:
            return l


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)

    data = [int(x) for x in lines[0].split(',')]

    print(f"data: {len(data)} lines: {len(lines)}")
    print(data)

    if part == 1:
        r = _part_one(data, 2020)
        print('part 1: ' + str(r))
    elif part == 2:
        r = _part_one(data, 30000000)
        print('part 2: ' + str(r))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

