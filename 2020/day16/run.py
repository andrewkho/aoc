import fire
from typing import *
import re
import itertools
from collections import deque

from dataclasses import dataclass, field
import numpy as np


def _part_one(data):
    c = 0
    for t in data['nearby_tickets']:
        for v in t:
            if all(not r.is_valid(v) 
                   for r in data['rules']):
                c += v

    return c


def _part_two(data):
    """
    After determining the valid tickets,
    this problem can be solved by solving the 
    bipartite matching problem between rules and fields
    where the path from rule r and field f exists only
    if the r is valid for field f in all tickets. 

    The bipartite matching problem can be solved as a maximum
    flow.
    """
    valid_neighbours = []
    for t in data['nearby_tickets']:
        valid = True
        for f in t:
            if all(not r.is_valid(f) 
                   for r in data['rules']):
                valid = False
                break

        if valid:
            valid_neighbours.append(t)

    matches = _get_valid_rules(data["rules"], valid_neighbours)
    print(matches)

    prod = 1
    print(f'your_ticket: {data["your_ticket"]}')
    for rule_name, f in matches.items():
        if rule_name.startswith('departure'):
            prod *= data['your_ticket'][f]

    return prod


from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow


def _get_valid_rules(rules, tickets) -> Dict[str, int]:
    # Let's try this using maxflow
    R = len(rules)
    T = len(tickets)
    # F is just number of rules
    F = R

    N = 1 + R + F + 1

    C = np.zeros((N, N), dtype=int)
    
    # Initialize arcs from source to tickets
    src = 0
    snk = N-1

    def rule_index(r):
        return 1 + r

    def field_index(f):
        return 1 + R + f

    # source to rule
    for r in range(R):
        C[src, rule_index(r)] = 1

    # fields to snk
    for f in range(F):
        C[field_index(f), snk] = 1

    # rules
    for r in range(R):
        for f in range(F):
            valid = all(
                rules[r].is_valid(t[f])
                for t in tickets
            )

            if not valid:
                continue
            C[rule_index(r), field_index(f)] = 1

    print(f"dims: T: {T}, F: {F}, R: {R}, N: {N}")
    print(C)

    print("Converting to CSR...")
    C = csr_matrix(C)

    print(f"Solving max flow for matrix shape {C.shape}...")

    result = maximum_flow(C, src, snk)

    print(f"result: {result.flow_value}")
    
    if (result.flow_value != R):
        print(f"Uh oh, not enough flow!")

    residual = result.residual

    matches = dict()
    for r in range(R):
        for f in range(F):
            try:
                if residual[rule_index(r), field_index(f)] == 1:
                    rule = rules[r]
                    if rule.name in matches:
                        raise ValueError()
                    matches[rule.name] = f
            except KeyError:
                continue

    if not set(range(F)) == set(matches.values()):
        print("Error: Invalid matching!")

    return matches


@dataclass
class Rule:
    name: str
    r1: Tuple[int, int]
    r2: Tuple[int, int]

    def is_valid(self, num):
        return (
            (self.r1[0] <= num <= self.r1[1]) or 
            (self.r2[0] <= num <= self.r2[1])
        )


def _parse_lines(lines):
    rules = []
    tickets = []

    for i, line in enumerate(lines):
        if line.strip() == '':
            break
        name, r = line.strip().split(':')
        r1, r2 = r.split('or')
        r1 = r1.strip().split('-')
        r2 = r2.strip().split('-')
        
        r1 = (int(r1[0].strip()), int(r1[1].strip()))
        r2 = (int(r2[0].strip()), int(r2[1].strip()))

        rules.append(Rule(name, r1, r2))

    for line in lines[i+1:]:
        if line[0].isnumeric():
            ticket = [int(x) for x in line.strip().split(',')]
            tickets.append(ticket)

    return {
        "rules": rules,
        "your_ticket": tickets[0],
        "nearby_tickets": tickets[1:],
    }


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)

    data = _parse_lines(lines)

    print(f"data: {len(data)} lines: {len(lines)}")
    print(data)

    if part == 1:
        r = _part_one(data)
        print('part 1: ' + str(r))
    elif part == 2:
        r = _part_two(data)
        print('part 2: ' + str(r))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

