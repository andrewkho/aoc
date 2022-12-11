from typing import *
from timer import Timer
import copy
import re
from dataclasses import dataclass, field
import math
from collections import deque


@dataclass
class Monkey:
    items: List[int]
    op: str
    test: int
    t: int
    f: int


def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        with open(infile, "r") as f:
            lines = [line.strip() for line in f.readlines()]

        i = 0
        monkeys = []
        while i < len(lines):
            i+=1
            _, items = lines[i].split(":")
            items = [int(x.strip()) for x in items.strip().split(",")]
            i+=1
            _, op = lines[i].split('=')
            op = op.strip().split(' ')
            i+=1
            _, test = lines[i].split(" divisible by ")
            test = int(test.strip())
            i+=1
            t = int(lines[i][-1])
            i+=1
            f = int(lines[i][-1])
            i+=1
            i+=1
            monkeys.append(Monkey(items, op, test, t, f))

        monkeys2 = copy.deepcopy(monkeys)

    def play(monkeys, rounds, div) -> List[int]:
        mod = 1
        for monkey in monkeys:
            mod *= monkey.test
        inspects = [0]*len(monkeys)
        for rnd in range(rounds):
            for i, monkey in enumerate(monkeys):
                for item in monkey.items:
                    inspects[i] += 1
                    op = monkey.op
                    right = int(op[2]) if op[2].isnumeric() else item
                    if op[1] == '*':
                        new = ((item*right) // div) % mod
                    else: # '+'
                        new = ((item+right) // div) % mod

                    if new % monkey.test == 0:
                        monkeys[monkey.t].items.append(new)
                    else:
                        monkeys[monkey.f].items.append(new)
                monkey.items.clear()
        return inspects
    
    with Timer("part 1"):
        inspects = play(monkeys, 20, 3)
        inspects = sorted(inspects, reverse=True)
        print("part 1:", inspects[0]*inspects[1])

    with Timer("part 2"):
        inspects = play(monkeys2, 10000, 1)
        inspects = sorted(inspects, reverse=True)
        print("part 2:", inspects[0]*inspects[1])


if __name__ == '__main__':
    main()
