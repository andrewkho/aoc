from typing import *
from timer import Timer
import copy
import re
from dataclasses import dataclass, field
import math
from collections import deque, defaultdict

import itertools
import functools


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    matcher = re.compile(r'^Blueprint [0-9]+: .* ([0-9]) .* ([0-9]) .* ([0-9]+) .* ([0-9]+) .* ([0-9]+) .* ([0-9]+) .*$')
    with Timer(f"Reading from {infile}..."):
        recipes = []
        with open(infile, "r") as f:
            for line in f.readlines():
                m = matcher.match(line.strip())
                if not m:
                    raise ValueError(line)
                groups = m.groups()
                recipes.append(
                    [
                        (int(groups[0]), 0, 0),
                        (int(groups[1]), 0, 0),
                        (int(groups[2]), int(groups[3]), 0),
                        (int(groups[4]), 0, int(groups[5])),
                    ]
                )
    print(recipes)

    with Timer("part 1"):
        @functools.lru_cache(maxsize=None)
        def dfs(minutes, ridx, bots, counts):
            nonlocal bestest
            if minutes == 0:
                if counts[3] > bestest:
                    bestest = counts[3]
                return counts[3]
            if bestest >= counts[3] + bots[3]*minutes + sum(range(minutes)):
                return -1
            new_counts = list(counts)
            for i, b in enumerate(bots):
                new_counts[i] += b

            best = 0
            new_bots = list(bots)
            for i in range(3, -1, -1):
                if i<3 and bots[i] >= max(cost[i] for cost in recipes[ridx]):
                    # Don't make more bots than you need to make any other bot
                    continue
                cost = recipes[ridx][i]
                if all(counts[j] >= c for j, c in enumerate(cost)):
                    for j, c in enumerate(cost):
                        new_counts[j] -= c
                    new_bots[i] += 1
                    best = max(
                        best,
                        dfs(minutes-1, ridx, tuple(new_bots), tuple(new_counts))
                    )
                    new_bots[i] -= 1
                    for j, c in enumerate(cost):
                        new_counts[j] += c

            best = max( 
                best,
                dfs(minutes-1, ridx, bots, tuple(new_counts))
            )
            return best

        total = 0
        for i, recipe in enumerate(recipes):
            bestest = 0
            print(dfs.cache_info())
            dfs.cache_clear()
            total += (i+1)*dfs(24, i, (1, 0, 0, 0), (0, 0, 0, 0))
            print(i, total)

        print("part 1:", total)

    with Timer("part 2"):
        total = 1
        for i, recipe in enumerate(recipes[:3]):
            bestest = 0
            print(dfs.cache_info())
            dfs.cache_clear()
            total *= dfs(32, i, (1, 0, 0, 0), (0, 0, 0, 0))
            print(i, total)
        print("part 2:", total)


if __name__ == '__main__':
    main()
