from timer import Timer
from utils import get_input, Grid
from collections import defaultdict, Counter
import itertools

import re


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        tot = 0
        for y, line in enumerate(lines):
            i = 0
            g = Grid(len(line), len(lines))
            while i < len(line):
                if not line[i].isnumeric():
                    i += 1
                    continue
                j = i+1
                while (j+1 <= len(line)) and line[i:j+1].isnumeric():
                    j += 1
                
                for x, dy in itertools.product(range(i-1, j+1), [-1, 0, 1]):
                    if not 0 <= x < len(line):
                        continue
                    if not 0 <= y+dy < len(lines):
                        continue
                    check = lines[y+dy][x]
                    if not check.isnumeric() and check != ".":
                        tot += int(line[i:j])
                        break
                i = j+1

        print("part1:", tot)

    with Timer("part 2"):
        gears = defaultdict(list)
        for y, line in enumerate(lines):
            i = 0
            while i < len(line):
                if not line[i].isnumeric():
                    i += 1
                    continue
                j = i+1
                while (j+1 <= len(line)) and line[i:j+1].isnumeric():
                    j += 1

                for x, dy in itertools.product(range(i-1, j+1), [-1, 0, 1]):
                    if not 0 <= x < len(line):
                        continue
                    if not 0 <= y+dy < len(lines):
                        continue
                    if lines[y+dy][x] == "*":
                        gears[y+dy, x].append(int(line[i:j]))
                i = j+1

        tot = 0
        for vals in gears.values():
            if len(vals) == 2:
                tot += vals[0]*vals[1]

        print("part 2:", tot)


if __name__ == '__main__':
    main()
