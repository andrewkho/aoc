from timer import Timer
import utils
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
        inst = lines[0]
        hm = {}
        for line in lines[2:]:
            # key, lr = line.split(" = ")
            m = re.match(r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)", line)
            groups = m.groups()
            hm[groups[0]] = (groups[1], groups[2])
        
        result = 0
        node = "AAA"
        it = itertools.cycle(inst)
        while node != "ZZZ":
            node = hm[node][{"L": 0, "R": 1}[next(it)]]
            result += 1

        print("part1:", result)

    with Timer("part 2"):
        result = 0
        nodes = [node for node in hm if node[-1] == "A"]
        dists = [0]*len(nodes)
        it = itertools.cycle(inst)
        while any(d == 0 for d in dists):
            next_inst = 0 if next(it) == "L" else 1
            result += 1
            for i in range(len(nodes)):
                nodes[i] = hm[nodes[i]][next_inst]
                if dists[i] == 0 and nodes[i][-1] == "Z":
                    dists[i] = result

        primes = utils.get_primes(max(dists))
        def prime_factors(x):
            fac = defaultdict(int)
            while x > 1:
                for c in primes:
                    while x % c == 0:
                        x //= c
                        fac[c] += 1
            return fac
        
        factors = [prime_factors(d) for d in dists]
        result = 1
        for prime in primes:
            v = max(factor.get(prime, 0) for factor in factors)
            result *= prime ** v

        print("part 2:", result)


if __name__ == '__main__':
    main()
