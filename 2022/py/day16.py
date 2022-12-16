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
        matcher = re.compile(r'^Valve (.*) has flow rate=([0-9]+); tunnel(s?) lead(s?) to valve(s?) (.*)$')
        edges = {}
        flows = {}
        with open(infile, "r") as f:
            for line in f.readlines():
                m = matcher.match(line.strip())
                if not m:
                    raise ValueError(line)
                groups = m.groups()
                node = groups[0]
                edges[node] = groups[-1].split(', ')
                flows[node] = int(groups[1])
        
        targets = [node for node, flow in flows.items() if flow > 0]
        
        adj = {}
        for src in targets + ["AA"]:
            dq = deque()
            visited = {src}
            for nei in edges[src]:
                dq.append((nei, 1))
                visited.add(nei)
            while len(dq) > 0:
                node, dist = dq.popleft()

                if flows[node] > 0:
                    adj[src, node] = dist
                for nei in edges[node]:
                    if nei in visited:
                        continue
                    visited.add(nei)
                    dq.append((nei, dist+1))

    with Timer("part 1"):
        @functools.lru_cache(maxsize=None)
        def dfs(node, minutes, remaining):
            best = 0
            for nei in remaining:
                dist = adj[node, nei]
                t2 = minutes-dist-1
                if t2 < 0:
                    continue
                val =  t2*flows[nei] + dfs(nei, t2, remaining - {nei})
                if val > best:
                    best = val
            return best
        best = dfs("AA", 30, frozenset(targets))
        print("part 1:", best)

    with Timer("part 2"):
        @functools.lru_cache(maxsize=None)
        def dfs2(node, minutes, remaining):
            best = 0
            for nei in remaining:
                dist = adj[node, nei]
                t2 = minutes-dist-1
                if t2 < 0:
                    continue
                # take it or don't 
                best = max(
                    best,
                    t2*flows[nei] + dfs2(nei, t2, remaining - {nei}),
                    dfs("AA", 26, remaining), # for some reason this is faster here
                )
            return best 

        best = dfs2("AA", 26, frozenset(targets))
        print("part 2:", best)


if __name__ == '__main__':
    main()
