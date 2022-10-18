import math
import fire
from typing import *
import re
import itertools
from collections import deque

from dataclasses import dataclass, field
import numpy as np


@dataclass
class Cup:
    val: int
    next: 'Cup'


def _play(cur, steps, cup_max, pointers):
    for _ in range(steps):
        if _ % 10000 == 0:
            print(f"step {_}")

        pu = []
        tmp = cur.next
        for i in range(3):
            pu.append(tmp)
            tmp = tmp.next

        cur.next = tmp
        dest = cur.val - 1
        
        missing_vals = [p.val for p in pu]
        while dest in missing_vals or dest < 1:
            dest -= 1
            if dest < 1:
                dest = cup_max
        
        ins = pointers[dest]

        new_next = ins.next
        ins.next = pu[0]
        pu[2].next = new_next

        cur = cur.next


def _part_one(data, steps):
    cup_max = max(data)
    first = Cup(data[0], None)
    pointers = [None]*(len(data)+1)
    pointers[first.val] = first

    cur = first
    for d in data[1:]:
        c = Cup(d, None)
        pointers[d] = c
        cur.next = c
        cur = c

    cur.next = first
    cur = first

    _play(cur, steps, cup_max, pointers)

    return pointers[1]


def run(fname: str, part: int, rounds: int):
    data = [int(i) for i in str(fname)]

    print(str(data))

    if part == 1:
        one = _part_one(data, rounds)
        cur = one
        result = []
        while cur.next is not one:
            cur = cur.next
            result.append(cur.val)
        r = ''.join([str(r) for r in result])

        print(f'part {part}: ' + str(r))
    elif part == 2:
        one = _part_one(data + list(range(max(data)+1, 1_000_001)), rounds)
        r = one.next.val * one.next.next.val
        print(f'part {part}: ' + str(r))


if __name__ == '__main__':
    fire.Fire(run)

