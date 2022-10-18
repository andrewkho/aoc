import math
import fire
from typing import *
import re
import itertools
from collections import deque

from dataclasses import dataclass, field
import numpy as np


def _parse_allergens(data):
    c = dict()
    for r in data:
        for a in r.alg:
            if a not in c:
                c[a] = set(r.ing)
            else:
                c[a].intersection_update(r.ing)

    return c


def _part_one(data):
    c = _parse_allergens(data)

    I = set()
    for r in data:
        I.update(r.ing)

    for a, ing in c.items():
        I.difference_update(ing)

    count = 0
    for r in data:
        for ing in r.ing:
            if ing in I:
                count += 1

    return c, I, count


from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow

def _part_two(data):
    """
    Once again solve a matching problem with
    maxflow
    """

    c = _parse_allergens(data)

    allergens = sorted(c.keys())
    ingredients = set()
    for r in c.values():
        ingredients.update(r)
    ingredients = list(ingredients)

    print(allergens)
    print(ingredients)

    assert len(ingredients) == len(allergens)

    N = 1 + len(ingredients) + len(allergens) + 1
    def a_index(a):
        return 1 + a
    def i_index(i):
        return 1 + len(allergens) + i

    C = np.zeros([N, N], dtype=int)
    src = 0
    snk = N-1
    for a, alg in enumerate(allergens):
        C[src, a_index(a)] = 1  # src to left side
        print(a, alg, c[alg])
        for ing in c[alg]:
            i = ingredients.index(ing)
            C[a_index(a), i_index(i)] = 1

    for i in range(len(ingredients)):
        C[i_index(i), snk] = 1  # rhs to sink

    print(C)
    
    result = maximum_flow(csr_matrix(C), src, snk)

    assert result.flow_value == len(ingredients), result

    print(f"flow_value: {result.flow_value}")

    answer = []
    for a, alg in enumerate(allergens):
        for ing in c[alg]:
            i = ingredients.index(ing)
            if result.residual[a_index(a), i_index(i)] == 1:
                answer.append(ing)
                break

    return ','.join(answer)


@dataclass
class Recipe:
    ing: List[str]
    alg: List[str]


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    data = []
    parser = re.compile(r'^(.*) \(contains (.*)\)$')
    for line in lines:
        m = parser.match(line)
        ing = [_.strip() for _ in m.group(1).split(' ')]
        alg = [_.strip() for _ in m.group(2).split(',')]
        data.append(Recipe(ing, alg))

    print(str(data))

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

