import multiprocessing as mp
from typing import *
from timer import Timer
import utils
from utils import get_input, Grid
from collections import defaultdict, Counter
import itertools
import bisect
import functools
import copy

import re


def dfs(vents: List[str], inst: Tuple[int], i: int = 0, groups = None, cur = 0, cache = None):
    groups = groups or []

    key = ("".join(vents[i:]), tuple(groups), cur)
    if key in cache:
        return cache[key]
    elif i == len(vents):
        if cur > 0:
            groups.append(cur)
        if groups == inst:
            cache[key] = 1
        else:
            cache[key] = 0
    elif sum([1 for x in vents[i:] if x in "#?"]) + sum(groups) + cur < sum(inst):
        cache[key] = 0
    elif sum([1 for x in vents[i:] if x == "#"]) + sum(groups) + cur > sum(inst):
        cache[key] = 0
    else:
        tot = 0
        c = vents[i]
        if c == "?":
            vents[i] = "#"
            tot += dfs(vents, inst, i, groups.copy(), cur, cache=cache)
            vents[i] = "."
            tot += dfs(vents, inst, i, groups.copy(), cur, cache=cache)
            vents[i] = "?"
        elif c == "#":
            cur += 1
            tot += dfs(vents, inst, i+1, groups.copy(), cur, cache=cache)
        elif c == ".":
            if cur > 0:
                groups.append(cur)
                if len(groups) > len(inst) or groups != inst[:len(groups)]:
                    cache[key] = 0
                    return 0
                cur = 0
            tot += dfs(vents, inst, i+1, groups.copy(), cur, cache=cache)
        else:
            raise ValueError(c)

        cache[key] = tot
    return cache[key] 

def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())

    with Timer("part 1"):
        with mp.Pool(12) as pool:
            results = pool.map(run_dfs, lines)
        print("part1:", sum(results))

    with Timer("part 2"):
        with mp.Pool(12) as pool:
            results = pool.starmap(run_dfs, [(line, 5) for line in lines])
        print("part 2:", sum(results))

def run_dfs(line, mul=1):
    vents, inst = line.split(" ")
    vents = "?".join([vents]*mul)
    inst = ",".join([inst]*mul)
    vents = list(vents)
    inst = list(int(x) for x in inst.split(","))

    result = dfs(vents, inst, cache=dict())
    return result

if __name__ == '__main__':
    main()
