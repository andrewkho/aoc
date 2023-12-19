import multiprocessing as mp
from typing import *
from timer import Timer
import utils
from utils import get_input, Grid
from collections import defaultdict, Counter, deque
from dataclasses import dataclass, field
import itertools
import bisect
import functools
import copy
import heapq

import re


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())
    
    with Timer("part 1"):
        workflows = {}
        for i, line in enumerate(lines):
            if line.strip() == "":
                break
            m = re.match(r"(.*){(.*)}", line)
            name = m.groups()[0]
            conditions = m.groups()[1].split(",")
            workflows[name] = conditions

        parts = []
        for line in lines[i+1:]:
            part = {}
            for xmas in line[1:-1].split(","):
                part["xmas"[len(part)]] = int(xmas.split("=")[1])
            parts.append(part)

        result = 0
        for part in parts:
            cur = "in"
            while True:
                if cur == "A":
                    result += sum(part.values())
                    break
                elif cur == "R":
                    break

                conditions = workflows[cur]
                for rule in conditions:
                    if ":" not in rule:
                        cur = rule
                        break
                    cond, dest = rule.split(":")
                    if "<" in cond:
                        k = cond.split("<")[0]
                        v = int(cond.split("<")[1])
                        if part[k] < v:
                            cur = dest
                            break
                    elif ">" in cond:
                        k = cond.split(">")[0]
                        v = int(cond.split(">")[1])
                        if part[k] > v:
                            cur = dest
                            break
                    else:
                        raise ValueError(part, rule, cond)

        print("part1:", result)

    with Timer("part 2"):
        result = 0
        def dfs(parts, cur = "in"):
            if cur == "A":
                result = 1
                for v in parts.values():
                    result *= v[1] - v[0] + 1
                return result
            elif cur == "R":
                return 0

            conditions = workflows[cur]
            result = 0
            for rule in conditions:
                if ":" not in rule:
                    result += dfs(parts, rule)
                    break
                cond, dest = rule.split(":")
                if "<" in cond:
                    k = cond.split("<")[0]
                    v = int(cond.split("<")[1])
                    if parts[k][1] < v:
                        result += dfs(parts, dest)
                        break
                    elif parts[k][0] >= v:
                        break
                    else:
                        left, right = parts.copy(), parts.copy()
                        left[k] = (parts[k][0], v-1)
                        right[k] = (v, parts[k][1])
                        result += dfs(left, dest)
                        parts = right
                elif ">" in cond:
                    k = cond.split(">")[0]
                    v = int(cond.split(">")[1])
                    if parts[k][0] > v:
                        result += dfs(parts, dest)
                        break
                    elif parts[k][1] > v:
                        left, right = parts.copy(), parts.copy()
                        left[k] = (parts[k][0], v)
                        right[k] = (v+1, parts[k][1])
                        result += dfs(right, dest)
                        parts = left
                    else:
                        break
                else:
                    raise ValueError(part, rule, cond)

            return result 

        print("part 2:", dfs({k: (1, 4000) for k in "xmas"}))


if __name__ == '__main__':
    main()
