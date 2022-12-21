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

    with Timer(f"Reading from {infile}..."):
        monkeys = dict()
        instrs = dict()
        graph = defaultdict(set)
        indegree = defaultdict(lambda: 0)
        with open(infile, "r") as f:
            for line in f.readlines():
                monkey, instr = line.strip().split(':')
                if instr.strip().isnumeric():
                    monkeys[monkey] = int(instr.strip())
                else:
                    m = re.match(r'(\w+) (.*) (\w+)', instr.strip())
                    if not m:
                        raise ValueError(line)
                    indegree[monkey] += 2
                    instrs[monkey] = [g.strip() for g in m.groups()]
                    graph[instrs[monkey][0].strip()].add(monkey)
                    graph[instrs[monkey][2].strip()].add(monkey)

        orig = copy.deepcopy(monkeys)
        
    with Timer("part 1"):
        stack = []
        for monkey in monkeys:
            for other in graph[monkey]:
                indegree[other] -= 1
                if indegree[other] == 0:
                    stack.append(other)
        while stack:
            monkey = stack.pop()
            l, op, r = instrs[monkey]
            l, r = monkeys[l], monkeys[r]
            if op == '+': monkeys[monkey] = l+r
            elif op == '-': monkeys[monkey] = l-r
            elif op == '*': monkeys[monkey] = l*r
            elif op == '/': monkeys[monkey] = l//r
            for other in graph[monkey]:
                indegree[other] -= 1
                if indegree[other] == 0:
                    stack.append(other)

        print("part 1:", monkeys["root"])

    with Timer("part 2"):
        monkeys = orig

        @functools.lru_cache(maxsize=None)
        def dfs(monkey):
            if monkey == 'humn':
                return None
            elif monkey in monkeys:
                return monkeys[monkey]

            l, op, r = instrs[monkey]
            lv, rv = dfs(l), dfs(r)
            if lv is None or rv is None: return None
            elif op == '+': return lv +  rv
            elif op == '-': return lv -  rv
            elif op == '*': return lv *  rv
            elif op == '/': return lv // rv

        def srch(monkey, target):
            if monkey == "humn":
                return target
            l, op, r = instrs[monkey]
            lv = dfs(l)
            rv = dfs(r)
            
            if op == '+':
                if lv is None: return srch(l, target-rv)
                else:          return srch(r, target-lv)
            elif op == '-':
                if lv is None: return srch(l, target+rv)
                else:          return srch(r, lv-target)
            elif op == '*':
                if lv is None: return srch(l, target//rv)
                else:          return srch(r, target//lv)
            elif op == '/':
                if lv is None: return srch(l, target*rv)
                else:          return srch(r, lv//target)

        left = dfs(instrs["root"][0])
        right = dfs(instrs["root"][2])
        if left is None:
            result = srch(instrs["root"][0], right)
        else:
            result = srch(instrs["root"][2], left)

        print("part 2:", result)


if __name__ == '__main__':
    main()
