import fire
from typing import *
from dataclasses import dataclass



TREE = '#'
NOTREE = '.'

def _part_one(data, offset, offset_row):
    trees = 0

    data2 = [
        data[i]
        for i in range(0, len(data), offset_row)
    ]

    for i, row in enumerate(data2):
        if row.char_at(i*offset) == TREE:
            trees += 1

    return trees


def _part_two(data, offsets, offset_rows):
    trees_hit = [
        _part_one(data, offset, offset_row)
        for offset, offset_row in zip(offsets, offset_rows)
    ]

    product = 1
    for x in trees_hit:
        product *= x

    print(f"trees_hit: {trees_hit}")
    print(f"product: {product}")


@dataclass
class RepeatedRow:
    seed: str

    def char_at(self, i: int):
        return self.seed[i%len(self.seed)]
    

def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    length = len(lines[0].strip())

    def process_line(line):
        l = line.strip()
        if len(l) != length:
            raise ValueError(f"Bad lengths! {l}, {len(l)}, {length}")
        return RepeatedRow(l)
        
    data = [process_line(line) for line in lines]

    print(data)
    print(f"data: {len(data)} lines: {len(lines)}")

    if part == 1:
        print(_part_one(data, 3, 1))
    elif part == 2:
        _part_two(data, 
                  [1, 3, 5, 7, 1],
                  [1, 1, 1, 1, 2])
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)
