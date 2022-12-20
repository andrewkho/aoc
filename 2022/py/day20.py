from typing import *
from timer import Timer
import copy
import re
from dataclasses import dataclass, field
import math
from collections import deque, defaultdict

import itertools
import functools


@dataclass
class Node:
    val: int
    left: 'Node' = None
    right: 'Node' = None

def main():
    infile = "../inputs/" + __file__.replace(".py", ".txt")

    with Timer(f"Reading from {infile}..."):
        def read_file():
            zero = None
            nodes = []
            with open(infile, "r") as f:
                for line in f.readlines():
                    n = int(line.strip())
                    node = Node(n)
                    if len(nodes) > 0:
                        node.left = nodes[-1]
                        nodes[-1].right = node
                    nodes.append(node)
                    if n == 0:
                        zero = node

                nodes[-1].right = nodes[0]
                nodes[0].left = nodes[-1]
            return nodes, zero

    with Timer("part 1"):
        def mix(mult, nodes):
            for n in nodes:
                n.left.right, n.right.left = n.right, n.left
                steps = (n.val*mult) % (len(nodes)-1)
                nxt = n.right
                for _ in range(steps):
                    nxt = nxt.right
                prv = nxt.left
                n.left, n.right = prv, nxt
                prv.right, nxt.left = n, n
        
        nodes, zero = read_file()
        mix(1, nodes)
        results = []
        n = zero
        for _ in range(3):
            for _ in range(1000):
                n = n.right
            results.append(n.val)
        print("part 1:", sum(results), results)

    with Timer("part 2"):
        nodes, zero = read_file()
        for _ in range(10):
            mix(811589153, nodes)

        results = []
        n = zero
        for _ in range(3):
            for _ in range(1000):
                n = n.right
            results.append(n.val*811589153)
        print("part 2:", sum(results), results)


if __name__ == '__main__':
    main()
