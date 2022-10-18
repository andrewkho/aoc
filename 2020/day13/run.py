import fire
from typing import *
import re
import numpy as np
from collections import deque
from dataclasses import dataclass, field


def _part_one(start, data):
    busses = [int(x) for x in data if x.isnumeric()]
    print(start)
    print(busses)

    nearest_bus = None
    time_to_next = max(busses)+1
    for bus in busses:
        t = bus - start%bus
        if t < time_to_next:
            nearest_bus = bus
            time_to_next = t

    print(f"nearest_bus: {nearest_bus}, time_to_next: {time_to_next}")
    return nearest_bus*time_to_next



def _part_two(data):
    """
    for the example: {7: 0, 13: 1, 59: 4, 31: 6, 19: 7}
    find the minimum time t s.t. 
        (t + 0) % 7 == 0
        (t + 1) % 13 == 0
        (t + 4) % 59 == 0
        (t + 6) % 31 == 0
        (t + 7) % 19 == 0

    (solution 1068781)
    
    One approach is to start with the biggest bus number
    59, and start with 59-4, 2*59-4, 3*59-4, etc
    and for each check that if other schedules are satisfied

    see the chinese remainder solution in v4
    """
    sched = {
        int(x): i
        for i, x in enumerate(data)
        if x.isnumeric()
    }

    busses = sorted(sched.keys(), reverse=True)

    d = busses[0]
    t = d - sched[d]
    i = 0
    while True:
        if i % 100_000 == 0:
            print(f"i: {i}")

        fail = False
        for bus in busses[1:]:
            if (t + sched[bus]) % bus != 0:
                fail = True
                break

        if not fail:
            break

        t += d
        i += 1

    return t


def _build_model(remainders):

    A = list(remainders.keys())
    R = list(remainders.values())

    model = pyo.ConcreteModel()
    model.x = pyo.Var(range(len(A)), domain=pyo.NonNegativeIntegers)
    model.obj = pyo.Objective(expr = model.x[0])

    model.c = pyo.ConstraintList()

    #sched = {59: 0, 31: 30, 19: 5, 13: 4, 7: 6}

    for i, (a, r) in enumerate(zip(A[1:], R[1:])):
        model.c.add(expr=A[0]*model.x[0] - a*model.x[i+1] == -r)

    return model


def _part_two_v2(data, solver='cplex'):
    """
    Set this up as a constrained optimization integer program
    (Fails to converge, too slow or maybe values of solution too big?)
    """
    sched = {
        int(x): i
        for i, x in enumerate(data)
        if x.isnumeric()
    }

    busses = sorted(sched.keys(), reverse=True)

    import pyomo.environ as pyo
    
    # First time
    t = busses[0] - sched[busses[0]]

    remainders = {x: (t+sched[x]) % x for x in busses}

    print(remainders)
    
    model = _build_model(remainders)

    opt = pyo.SolverFactory(solver)

    print(opt.solve(model))
    t += pyo.value(model.x[0]) * busses[0]
    
    return t


def _part_two_v4(data):
    """
    Just use the chinese remainder theorem
    """
    sched = {
        int(x): i
        for i, x in enumerate(data)
        if x.isnumeric()
    }

    busses = list(sched.keys())

    def valid_solution(t):
        return all((t+sched[x]) % x == 0 
                   for x in busses)

    Ms = list(sched.keys())
    # We have the inverse remainders
    As = [k-v for k, v in sched.items()]
    M = 1
    for m in Ms:
        M *= m
    
    Bs = [M // m for m in Ms]

    def inv(_b, _m):
        _b = _b % _m
        x = 1
        while True:
            if (x*_b) % _m == 1:
                return x
            x += 1

    Ps = [ inv(*_) for _ in zip(Bs, Ms) ]

    p = [ a*b*p for a, b, p in zip(As, Bs, Ps)]

    t = sum(p) % M

    print(f"check solution: {valid_solution(t)}")

    return t


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)
    start = int(lines[0].strip())
    data = [_.strip() 
            for _ in lines[1].strip().split(',')]

    print(f"data: {len(data)} lines: {len(lines)}")
    print(data)

    if part == 1:
        r = _part_one(start, data)
        print('part 1: ' + str(r))
    elif part == 2:
        r = _part_two_v4(data)
        print('part 2: ' + str(r))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

