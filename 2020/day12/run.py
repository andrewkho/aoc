import fire
from typing import *
import re
import numpy as np
from collections import deque
from dataclasses import dataclass, field


DIRS = ['N', 'E', 'S', 'W']

def _part_one(data):
    
    pos = [0, 0]
    facing = 1
    
    for inst in data:
        if inst.op in {'L', 'R'}:
            # we can rotate around the compass with modulo
            if inst.val % 90 != 0: 
                raise ValueError(f"Bad instruction: {inst.op}{inst.val}")
            shift = int(inst.val // 90)
            if inst.op == 'L':
                shift *= -1 
            facing = (facing + shift) % 4
            continue

        if inst.op == 'F':
            mv = DIRS[facing]
        elif inst.op in {'N', 'S', 'E', 'W'}:
            mv = inst.op
        else:
            raise ValueError(f"invalid op {inst.op}{inst.val}")

        if mv == 'E':
            pos[0] += inst.val
        elif mv == 'W':
            pos[0] -= inst.val
        elif mv == 'N':
            pos[1] += inst.val
        elif mv == 'S':
            pos[1] -= inst.val
            

    print(f"pos: {pos}")

    return abs(pos[0]) + abs(pos[1])


def _part_two(data):
    
    pos = [0, 0]
    way = [10, 1]
    
    for inst in data:
        if inst.op in {'L', 'R'}:
            if inst.val == 180:
                way = [-way[0], -way[1]]
            elif (inst.val == 90 and inst.op == 'R') or \
                 (inst.val == 270 and inst.op == 'L'):
                way = [way[1], -way[0]]
            elif (inst.val == 90 and inst.op == 'L') or \
                 (inst.val == 270 and inst.op == 'R'):
                way = [-way[1], way[0]]
            else:
                raise ValueError(f"Bad instruction: {inst.op}{inst.val}")

            continue

        if inst.op == 'F':
            pos[0] += way[0]*inst.val
            pos[1] += way[1]*inst.val
            continue

        if inst.op in {'N', 'S', 'E', 'W'}:
            mv = inst.op
        else:
            raise ValueError(f"invalid op {inst.op}{inst.val}")

        if mv == 'E':
            way[0] += inst.val
        elif mv == 'W':
            way[0] -= inst.val
        elif mv == 'N':
            way[1] += inst.val
        elif mv == 'S':
            way[1] -= inst.val
            

    print(f"pos: {pos}, way: {way}")

    return abs(pos[0]) + abs(pos[1])


@dataclass
class Instruction:
    op: str
    val: int


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)
    data = [Instruction(line[0], int(line.strip()[1:]))
            for line in lines]

    print(f"data: {len(data)} lines: {len(lines)}")
    print(data)

    if part == 1:
        r = _part_one(data)
        print('part 1: ' + str(r))
    elif part == 2:
        r = _part_two(data)
        print('part 2: ' + str(r))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

