from timer import Timer
from utils import get_input, Grid
from collections import defaultdict, Counter
import itertools
import bisect

import re


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        seeds = map(int, lines[0].split(":")[1].strip().split(" "))
        maps = {}
        src, dst = None, None
        for y, line in enumerate(lines[1:]):
            if not line.strip():
                continue
            elif all(x.isnumeric() for x in line.split(" ")):
                maps[src].append(tuple(int(x) for x in line.split(" ")))
            else:
                m = re.match(r"(.*)-to-(.*) map\:", line.strip())
                src, dst = m.groups()[0], m.groups()[1]
                maps[src] = [dst]

        for src, vals in maps.items():
            dst = vals[0]
            maps[src] = [dst] + sorted([(source, rang, dest) for dest, source, rang in vals[1:]])
        
        results = []
        for seed in seeds:
            src = "seed"
            while src != "location":
                dst, vals = maps[src][0], maps[src][1:]
                idx = bisect.bisect_right([x[0] for x in vals], seed) - 1
                source, rang, dest = vals[idx]
                if source <= seed < source + rang:
                    seed = dest + seed - source
                src = dst
            results.append(seed)

        print("part1:", min(results), results)

    with Timer("part 2"):
        seed_ranges = []
        seeds = list(map(int, lines[0].split(":")[1].strip().split(" ")))
        for i in range(0, len(seeds), 2):
            seed_ranges.append((seeds[i], seeds[i]+seeds[i+1]))
        
        # add all the 1:1 ranges to simplify dfs, will double length of ranges but same big-O compute
        for src, vals in maps.items():
            new_ranges = [vals[0]]
            ranges = vals[1:]
            if ranges[0][0] > 0:
                new_ranges.append((0, ranges[0][0], 0))
            for idx in range(len(ranges)):
                new_ranges.append(ranges[idx])
                source, rang, dest = ranges[idx]
                if idx + 1 == len(ranges):
                    # add final infinite range
                    new_ranges.append((source+rang, float('inf'), source+rang))
                elif source + rang < ranges[idx+1][0]:
                    new_ranges.append((source+rang, ranges[idx+1][0]-(source+rang), source+rang))
            maps[src] = new_ranges

        def search_range(src, lo, hi, bst=float("inf")):
            if src == "location":
                return min(lo, bst)
            dst, vals = maps[src][0], maps[src][1:]
            map_lo = bisect.bisect_right([x[0] for x in vals], lo) - 1
            map_hi = bisect.bisect_right([x[0] for x in vals], hi)
            for idx in range(map_lo, map_hi):
                source, rang, dest = vals[idx]
                new_lo = dest + max(source, lo) - source
                new_hi = dest + min(source+rang, hi) - source
                bst = search_range(dst, new_lo, new_hi, bst)
            return bst

        results = []
        for lo, hi in seed_ranges:
            results.append(search_range("seed", lo, hi))
        print("part 2:", min(results), results)


if __name__ == '__main__':
    main()
