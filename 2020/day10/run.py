import fire
from typing import *
import re
from collections import deque
from dataclasses import dataclass, field


def _part_one(data):

    data = [0] + sorted(data)
    data.append(data[-1]+3)

    diffs = [0]*4

    prev = data[0]
    for i in data[1:]:
        d = i - prev
        diffs[d] += 1
        prev = i

    print(diffs)

    return diffs[1] * diffs[3]


def _find_droppable(data, state):
    droppable = list()

    idx = [
        i for i, s in enumerate(state)
        if s == 1
    ]

    for i in range(1, len(idx)-1):
        l = idx[i-1]
        m = idx[i]
        r = idx[i+1]
        if data[r] - data[l] <= 3:
            droppable.append(m)

    return droppable


def _count_the_ways(data: List[int], state: Tuple[int], visited: Set[int]):
    visited.add(state)

    droppable = _find_droppable(data, state) 
    for d in droppable:
        new_state = state[:d] + (0,) + state[d+1:]
        assert len(state) == len(new_state)
        if new_state not in visited:
            _count_the_ways(data, new_state, visited)


def _part_two(data):
    data = [0] + sorted(data)
    data.append(data[-1]+3)

    state = tuple([1]*len(data))
    visited = set()

    _count_the_ways(data, state, visited)

    return len(visited)


def _find_droppable_v2(data, minimum):
    droppable = []
    for i in range(minimum, len(data)-1):
        if data[i+1] - data[i-1] <= 3:
            droppable.append(i)

    return droppable


def _count_the_ways_v2(data, i):
    droppable = _find_droppable_v2(data, i)
    
    c = len(droppable)

    for d in droppable:
        new_data = data[:d] + data[d+1:]
        
        c += _count_the_ways_v2(new_data, d)

    return c
    

def _part_two_v2(data):
    data = [0] + sorted(data)
    data.append(data[-1]+3)

    return 1 + _count_the_ways_v2(data, 1)


def _find_droppable_v3(data, droppable):
    new_droppable = []
    for i in droppable:
        if data[i+1] - data[i-1] <= 3:
            new_droppable.append(i)

    return new_droppable


def _count_the_ways_v3(data, droppable):
    droppable = _find_droppable_v3(data, droppable)
    
    c = len(droppable)

    for d in droppable:
        new_data = data[:d] + data[d+1:]

        c += _count_the_ways_v3(new_data, (x-1 for x in droppable if x > d))

    return c
    

def _part_two_v3(data):
    data = [0] + sorted(data)
    data.append(data[-1]+3)

    return 1 + _count_the_ways_v3(data, range(1, len(data)-1))


def _part_two_v4(data):
    data = [0] + sorted(data)
    data.append(data[-1]+3)

    ways = [0]*(max(data) + 1)
    ways[0] = 1

    for i in data[1:]:
        print(ways)
        s = ways[i-3] + ways[i-2] + ways[i-1]
        ways[i] = s

    return max(ways), ways


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)
    data = [int(line.strip()) for line in lines]

    print(f"data: {len(data)} lines: {len(lines)}")
    print(data)

    if part == 1:
        print('part 1: ' + str(_part_one(data)))
    elif part == 2:
        print('part 2: ' + str(_part_two_v4(data)))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

