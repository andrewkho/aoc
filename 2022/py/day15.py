from typing import *
from timer import Timer
import copy
import re
from dataclasses import dataclass, field
import math
from collections import deque

import itertools
import functools


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        sensors = []
        beacons = []
        matcher = re.compile(r'^Sensor at x=(-?[0-9]+), y=(-?[0-9]+): .* x=(-?[0-9]+), y=(-?[0-9]+)$')
        with open(infile, "r") as f:
            for line in f.readlines():
                m = matcher.match(line.strip())
                if not m:
                    raise ValueError(line)
                groups = m.groups()
                sensors.append((int(groups[0]), int(groups[1])))
                beacons.append((int(groups[2]), int(groups[3])))
    
    def merge_intervals(intervals):
        results = []
        for i in sorted(intervals):
            if results and i[0] <= results[-1][1]:
                results[-1][1] = max(results[-1][1], i[1])
            else:
                results.append(i)
        return results

    def scan_line(y):
        intervals = []
        for s, b in zip(sensors, beacons):
            d = abs(s[0]-b[0]) + abs(s[1]-b[1])
            dx = d-abs(y-s[1])
            if dx >= 0:
                intervals.append([s[0]-dx, s[0]+dx])
        return intervals

    with Timer("part 1"):
        intervals = scan_line(2000000)
        intervals = merge_intervals(intervals)
        total = sum(seg[1]-seg[0] for seg in intervals)
        print("part 1:", total)

    with Timer("part 2"):
        for y in range(0, 4000001):
            intervals = [[-float('inf'), -1], [4000001, float('inf')]]
            intervals += scan_line(y)
            intervals = merge_intervals(intervals)
            if len(intervals) > 1:
                x = intervals[0][1]+1
                break

        print("part 2:", y+4000000*x)


if __name__ == '__main__':
    main()
