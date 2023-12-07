from timer import Timer
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
        ORDER = "23456789TJQKA"
        def compare(h0, h1):
            h0, h1 = h0[0], h1[0]
            c0, c1 = Counter(h0), Counter(h1)
            p0 = list(reversed(sorted(c0.values()))) + [1]*(max(len(c0), len(c1)) - len(c0) + 1)
            p1 = list(reversed(sorted(c1.values()))) + [1]*(max(len(c0), len(c1)) - len(c0) + 1)
            for i in range(len(p0)):
                if p0[i] != p1[i]:
                    return p0[i]-p1[i]
            
            for i in range(len(h0)):
                if ORDER.index(h0[i]) != ORDER.index(h1[i]):
                    return ORDER.index(h0[i]) - ORDER.index(h1[i])

            return 0

        vals = sorted((tuple(line.split(" ")) for line in lines), key=functools.cmp_to_key(compare))
        result = 0
        for i, (_, v) in enumerate(vals):
            result += (i+1)*int(v)

        print("part1:", result)

    with Timer("part 2"):
        ORDER = "J23456789TQKA"
        def compare(h0, h1):
            h0, h1 = h0[0], h1[0]
            c0, c1 = Counter(h0), Counter(h1)
            j0, j1 = 0, 0
            if "J" in c0 and len(c0) > 1:
                j0 = c0.pop("J")
            if "J" in c1 and len(c1) > 1:
                j1 = c1.pop("J")
            p0 = list(reversed(sorted(c0.values()))) + [1]*(max(len(c0), len(c1)) - len(c0) + 1)
            p1 = list(reversed(sorted(c1.values()))) + [1]*(max(len(c0), len(c1)) - len(c0) + 1)
            p0[0] += j0
            p1[0] += j1
            for i in range(len(p0)):
                if p0[i] != p1[i]:
                    return p0[i]-p1[i]
            
            for i in range(len(h0)):
                if ORDER.index(h0[i]) != ORDER.index(h1[i]):
                    return ORDER.index(h0[i]) - ORDER.index(h1[i])

            return 0
        vals = sorted((tuple(line.split(" ")) for line in lines), key=functools.cmp_to_key(compare))
        result = 0
        for i, (_, v) in enumerate(vals):
            result += (i+1)*int(v)

        print("part 2:", result)


if __name__ == '__main__':
    main()
