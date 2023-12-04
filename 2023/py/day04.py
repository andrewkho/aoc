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
            _, line = line.split(":")
            card, numbers = line.split("|")
            card, numbers = line.split("|")
            left = {int(v) for v in card.strip().split(" ") if v}
            right = {int(v) for v in numbers.strip().split(" ") if v}
            ix = left.intersection(right)
            if len(ix) > 0:
                tot += 2**(len(ix) - 1)

        print("part1:", tot)

    with Timer("part 2"):
        copies = [1]*len(lines)
        for y, line in enumerate(lines):
            _, line = line.split(":")
            card, numbers = line.split("|")
            left = {int(v) for v in card.strip().split(" ") if v}
            right = {int(v) for v in numbers.strip().split(" ") if v}
            ix = left.intersection(right)
            for x in range(y+1, y+1+len(ix)):
                copies[x] += copies[y]

        print("part 2:", sum(copies))


if __name__ == '__main__':
    main()
