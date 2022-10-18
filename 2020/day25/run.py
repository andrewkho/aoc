import math
import fire
from typing import *
import re
import itertools
from collections import deque, defaultdict

from dataclasses import dataclass, field
import numpy as np


P = 20201227

def _handshake(pk):
    ln = 0
    v = 1
    sn = 7

    while True:
        if v == pk:
            return ln
        v = (v*sn) % P
        ln += 1


def _part_one(data):
    pk0 = data[0]
    pk1 = data[1]

    ln0 = _handshake(pk0)
    print(f'ln0: {ln0}')

    v = 1
    for _ in range(ln0):
        v = (v*pk1) % P
    print(f'encryption_key: {v}')

    ln1 = _handshake(pk1)
    print(f'ln1: {ln1}')

    v = 1
    for _ in range(ln1):
        v = (v*pk0) % P
    print(f'encryption_key: {v}')

    return v


def run(fname: str, part: int, steps: int=100):
    with open(fname, 'r') as f:
        lines = f.readlines()

    data = [int(line.strip()) for line in lines]

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

