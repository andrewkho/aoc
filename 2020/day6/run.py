import fire
from typing import *
from dataclasses import dataclass


def _part_one(data):
    counts = [len(group.keys()) for group in data]
    print(counts)
    return sum(counts)


def _part_two(data, sizes):
    total = 0
    for group, size in zip(data, sizes):
        yesses = []
        for char, count in group.items():
            if count == size:
                total += 1
                yesses.append(char)
        print(yesses)
    return total


def _parse_group(lines):
    group = dict()
    group_size = 0
    for i, line in enumerate(lines):
        if line.strip() == '':
            break
        group_size += 1
        for c in line.strip():
            if c not in group:
                group[c] = 0
            group[c] += 1

    return lines[i+1:], group, group_size


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)
    print(len(lines))

    data = []
    sizes = []
    while len(lines) > 0:
        lines, group, group_size = _parse_group(lines)
        data.append(group)
        sizes.append(group_size)

    print(data)
    print(f"data: {len(data)} lines: {len(lines)}")

    if part == 1:
        print('sum ' + str(_part_one(data)))
    elif part == 2:
        print('sum part 2 ' + str(_part_two(data, sizes)))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

