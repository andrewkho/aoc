import fire
from typing import *
import re
from collections import deque
from dataclasses import dataclass, field


def _part_one(data):
    acc = 0

    visited = [0] * len(data)
    curr = 0

    while True:
        if visited[curr] == 1:
            break

        visited[curr] = 1

        inst = data[curr]
        if inst.op == 'nop':
            curr += 1
        elif inst.op == 'acc':
            acc += inst.val
            curr += 1
        elif inst.op == 'jmp':
            curr += inst.val
        else:
            raise ValueError(f"invalid op: {inst.op}")

    if all(v == 1 for v in visited):
        raise ValueError("Visited every instruction!")

    return acc


def _check_for_cycle(data) -> Optional[int]:
    acc = 0

    visited = [0] * len(data)
    curr = 0
    while True:
        if curr >= len(data):
            return acc
        if visited[curr] == 1:
            return None

        visited[curr] = 1

        inst = data[curr]
        if inst.op == 'nop':
            curr += 1
        elif inst.op == 'acc':
            acc += inst.val
            curr += 1
        elif inst.op == 'jmp':
            curr += inst.val
        else:
            raise ValueError(f"invalid op: {inst.op}")


def _part_two(data):
    nops = [i for i, inst in enumerate(data) 
            if inst.op == 'nop']
    jmps = [i for i, inst in enumerate(data) 
            if inst.op == 'jmp']

    for nop in nops:
        modified = data[:nop]
        modified.append(Instruction('jmp', data[nop].val))
        modified.extend(data[nop+1:])

        assert len(modified) == len(data)

        result = _check_for_cycle(modified)
        if result is not None:
            print(f"Found no-cycle in nop {nop}")
            return result

    for jmp in jmps:
        modified = data[:jmp]
        modified.append(Instruction('nop', data[jmp].val))
        modified.extend(data[jmp+1:])

        assert len(modified) == len(data)

        result = _check_for_cycle(modified)
        if result is not None:
            print(f"Found no-cycle in jmp {jmp}")
            return result


@dataclass
class Instruction:
    op: str
    val: int


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)
    data = []
    for line in lines:
        op, valstr = line.strip().split(' ')
        op = op.strip()
        val = int(valstr.strip())

        instruction = Instruction(op, val) 
        data.append(instruction)

    print(f"data: {len(data)} lines: {len(lines)}")

    print(data)

    if part == 1:
        print('sum ' + str(_part_one(data)))
    elif part == 2:
        print('sum part 2 ' + str(_part_two(data)))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

