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


def bfs(states, gates, target, i = 0):
    q = deque([("broadcaster", "button", 0)])
    signals = [0, 0]
    hit = 0
    while q:
        cur, sender, sig = q.popleft()
        signals[sig] += 1
        if cur == target:
            states[cur] = sig
            if sig == 0:
                hit += 1
                # print(i, cur, sig)
            continue
        if cur not in gates:
            continue
        op, recvrs = gates[cur]
        if op == "broadcaster":
            for recv in recvrs:
                q.append((recv, cur, sig))
        elif op == "%" and sig == 0:
            states[cur] = 1 - states[cur]
            for recv in recvrs:
                q.append((recv, cur, states[cur]))
        elif op == "&":
            states[cur][sender] = sig
            if all(x == 1 for x in states[cur].values()):
                pulse = 0
            else:
                pulse = 1
            for recv in recvrs:
                q.append((recv, cur, pulse))
    return signals, hit


def get_new_states(gates):
    states = {}
    for k, (op, recvrs) in gates.items():
        if op == "%":
            states[k] = 0
        elif op == "&":
            states[k] = {}

    for k, (op, recvrs) in gates.items():
        for recv in recvrs:
            if recv in gates and gates[recv][0] == "&":
                states[recv][k] = 0
    return states


def main():
    infile = get_input(__file__)
    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = []
            for line in f.readlines():
                lines.append(line.strip())
    
    with Timer("part 1"):
        result = 0
        gates = {}
        for line in lines:
            l, r = line.split(" -> ")
            if l == "broadcaster":
                op = l
                name = l
            else:
                op = l[0]
                name = l[1:]
            gates[name] = (op, r.split(", "))

        signals = [0, 0]
        states = get_new_states(gates)
        for i in range(1000):
            result, _ = bfs(states, gates, "rx")
            signals[0] += result[0]
            signals[1] += result[1]
        print("part1:", signals[0]*signals[1])

    with Timer("part 2"):
        deps = defaultdict(list)
        for k, (op, recvrs) in gates.items():
            for recv in recvrs:
                deps[recv].append(k)

        goals = deps[deps["rx"][0]]
        bases = []
        print(f"{goals=}")
        for goal in goals:
            print(f"{goal=}")
            stack = [goal]
            new_gates = {}
            while stack:
                cur = stack.pop()
                if cur in new_gates:
                    continue
                new_gates[cur] = copy.deepcopy(gates[cur])
                for dep in deps[cur]:
                    if dep not in new_gates:
                        stack.append(dep)
            new_gates["broadcaster"] = ("broadcaster", [recv for recv in gates["broadcaster"][1] if recv in new_gates])
            states = get_new_states(new_gates)
            
            step = 0
            states = get_new_states(new_gates)
            while True:
                _, hit = bfs(states, new_gates, goal, step+1)
                step += 1
                if hit: 
                    bases.append(step)
                    break
                    
        print(bases)
        primes = utils.get_primes(max(bases))
        factors = [utils.prime_factors(d, primes) for d in bases]
        result = 1
        for prime in primes:
            v = max(factor.get(prime, 0) for factor in factors)
            result *= prime ** v

        print("part 2:", result)


if __name__ == '__main__':
    main()
