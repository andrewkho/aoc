from timer import Timer
import utils
from utils import get_input, Grid
from collections import defaultdict, Counter
import itertools
import bisect
import functools

import re


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        result = 0
        start = None
        for j, line in enumerate(lines):
            for i, c in enumerate(line):
                if c == 'S':
                    start = (j, i)
                    break 
            if start != None:
                break
        
        pnt, pdx = None, None
        lookup = {
            ((-1, 0), "|"): (-1, 0), ((1, 0), "|"): (1, 0),
            ((-1, 0), "7"): (0, -1), ((0, 1), "7"): (1, 0),
            ((-1, 0), "F"): (0, 1), ((0, -1), "F"): (1, 0),

            ((1, 0), "L"): (0, 1), ((0, -1), "L"): (-1, 0),
            ((1, 0), "J"): (0, -1), ((0, 1), "J"): (-1, 0),

            ((0, -1), "-"): (0, -1), ((0, 1), "-"): (0, 1),
        }
        start_neis = set()
        for ((dj, di), _), vals in lookup.items():
            pnt = (start[0]+dj, start[1]+di)
            pdx = (dj, di)
            if (pdx, lines[pnt[0]][pnt[1]]) in lookup:
                start_neis.add((dj, di))
        
        # Replace start line with correct char
        start_line = list(lines[start[0]])
        reverse_lookup = {
            "|": {(-1, 0), (1, 0)},
            "J": {(-1, 0), (0, -1)},
            "L": {(-1, 0), (0, 1)},
            "7": {(1, 0), (0, -1)},
            "F": {(1, 0), (0, 1)},
            "-": {(0, -1), (0, 1)},
        }
        for start_char, expected in reverse_lookup.items():
            if start_neis == expected:
                start_line[start[1]] = start_char
                break
        assert start_line[start[1]] != "S"
        lines[start[0]] = ''.join(start_line)

        pdx = next(iter(start_neis))
        pnt = (start[0] + pdx[0], start[1] + pdx[1])
        boundary = {start, pnt}
        dist = 1
        while pnt != start:
            pdx = lookup[pdx, lines[pnt[0]][pnt[1]]]
            pnt = (pnt[0] + pdx[0], pnt[1] + pdx[1])
            boundary.add(pnt)
            dist += 1

        print("part1:", dist//2 + dist%2)

    with Timer("part 2"):
        colours = [0, 0]
        for j, line in enumerate(lines):
            entry = None
            col = 0
            for i, c in enumerate(line):
                if (j, i) in boundary:
                    if c == "|":
                        col = 1 - col
                    elif entry is None:
                        entry = c
                    else:
                        if entry == "F" and c == "J":
                            col = 1 - col
                        elif entry == "L" and c == "7":
                            col = 1 - col
                        if c != "-":
                            entry = None
                else:
                    colours[col] += 1

        print("part 2:", colours[1], colours)


if __name__ == '__main__':
    main()
