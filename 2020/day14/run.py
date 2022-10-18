import fire
from typing import *
import re
import itertools
from collections import deque

from dataclasses import dataclass, field
import numpy as np


def _part_one(data):
    memory = dict()

    for inst in data:
        mask0 = int(inst.mask.replace('X', '1'), 2)
        mask1 = int(inst.mask.replace('X', '0'), 2)
        mv = (inst.value & mask0) | mask1
        memory[inst.address] = mv
        #print(memory)
    
    print(memory)

    return sum(memory.values())


def _get_indices(mask):
    indices = []
    i = 0
    while True:
        try:
            indices.append(mask.index('X', i))
            i = indices[-1] + 1
        except ValueError:
            break

    return indices


def _part_two(data):
    memory = dict()

    for inst in data:
        x_indices = _get_indices(inst.mask)
        for bits in itertools.product(*[['0', '1'] 
                                        for _ in x_indices]):
            mask0 = ['1']*len(inst.mask)
            mask1 = list(inst.mask.replace('X', '0'))
            for x, b in zip(x_indices, bits):
                if b == '0':
                    mask0[x] = b
                elif b == '1':
                    mask1[x] = b

            mask0 = ''.join(mask0)
            mask1 = ''.join(mask1)

            a = (inst.address & int(mask0, 2)) | int(mask1, 2)
            memory[a] = inst.value
    
    print(memory)

    return sum(memory.values())


@dataclass
class Instruction:
    mask: str
    address: int
    value: int


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)

    data = []
    mask = None
    for line in lines:
        l, r = line.split('=')
        l = l.strip()
        r = r.strip()
        
        if l == 'mask':
            mask = r
        elif l.startswith('mem'):
            address = int(l[len('mem['):-1])
            data.append(Instruction(mask, address, int(r)))
        else:
            raise ValueError(line)

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

