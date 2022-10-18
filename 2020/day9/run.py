import fire
from typing import *
import re
from collections import deque
from dataclasses import dataclass, field


def _check_valid(val, buffer):
    for i in range(len(buffer)):
        if buffer[i] > val:
            continue
        for j in range(i, len(buffer)):
            if buffer[i] + buffer[j] == val:
                return True

    return False

def _part_one(data, preamble):
    acc = 0

    for i in range(preamble, len(data)):
        buffer = data[i-preamble:i]
        val = data[i]

        if not _check_valid(val, buffer):
            break

    return data[i]


def _part_two(data, preamble):
    magic_num = _part_one(data, preamble)

    l = 0
    r = 1

    c = data[0]

    while c != magic_num:
        if c < magic_num:
            c += data[r]
            r += 1
        elif c > magic_num:
            c -= data[l]
            l += 1

    if c == magic_num:
        print(f"l: {l} r: {r} sum: {sum(data[l:r])}, data[l]: {data[l]}, data[r]: {data[r]}")

        return min(data[l:r]) + max(data[l:r])
    else:
        return None


def run(fname: str, part: int, preamble: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)
    data = [int(line.strip()) for line in lines]

    print(f"data: {len(data)} lines: {len(lines)}")
    print(data)

    if part == 1:
        print('part 1: ' + str(_part_one(data, preamble)))
    elif part == 2:
        print('part 2: ' + str(_part_two(data, preamble)))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

